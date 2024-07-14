
from django.http import HttpResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from . models import Pizza, Drinks, Cart, CartItem, OrderItems 
from . forms import OrderCreateForm, SearchForm
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def pizza_list(request):
    form = SearchForm(request.GET or None)
    pizzas = Pizza.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        pizzas = pizzas.filter(name__icontains=query)

    return render(request, 'dominozapp/pizza_list.html', {'pizzas': pizzas, 'form': form})

def pizza_detail(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    return render(request, 'dominozapp/pizza_detail.html', {'pizza': pizza})

 
def drink_list(request):
    form = SearchForm(request.GET or None)
    drinks = Drinks.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        drinks = drinks.filter(name__icontains=query)

    return render(request, 'dominozapp/drink_list.html', {'drinks': drinks, 'form': form})

def drink_detail(request, pk):
    drink = get_object_or_404(Drinks, pk=pk)
    return render(request, 'dominozapp/drink_detail.html', {'drink': drink})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'dominozapp/register.html', {'form':form})    
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pizza_list')
            else : 
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'dominozapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, item_type, item_id):
    user_cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    if item_type == 'pizza':
        item = get_object_or_404(Pizza, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, pizza=item)
    else:
        item = get_object_or_404(Drinks, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, drink=item)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    cart_items = CartItem.objects.filter(cart=cart) 
    total = sum(item.total for item in cart_items)
    print("total : ", total )
    return render(request, 'dominozapp/cart_detail.html', {'cart_items': cart_items, 'total': total})

@login_required
def increase_qunatity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

@login_required
def order_create(request):
    #cart = Cart.objects.get(id=1)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart.items.all():
                OrderItems.objects.create(
                    order = order,
                    drink = item.drink,
                    pizza = item.pizza,
                    price = item.drink.price if item.drink else item.pizza.price,
                    quantity = item.quantity
                )
            cart.items.all().delete()

            client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
            payment_data = {
                'amount': int(order.total_cost * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}', 
            }
            print(payment_data)
            payment = client.order.create(data=payment_data)
             
            return render(request, 'dominozapp/order_created.html', {'order': order, 'payment': payment, 'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID})
    else : 
        form = OrderCreateForm()
    return render(request, 'dominozapp/order_create.html', {'cart': cart, 'form': form})

@login_required
@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        return HttpResponse("Payment Successful")
    return HttpResponse(status=400)


























































































































    