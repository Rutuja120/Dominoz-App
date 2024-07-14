from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pizza(models.Model):

    image = models.ImageField(upload_to='pizzas/', blank=True, null=True)
    name= models.CharField(max_length=255) 
    size= models.CharField(max_length=255) 
    Topping= models.CharField(max_length=255)
    description = models.TextField()
     
    price = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return f"{self.name}"
    
class Drinks(models.Model):
    image = models.ImageField(upload_to='drinkss/', blank=True, null=True)
    name = models.CharField(max_length=255)
    size= models.CharField(max_length=255) 
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.name}"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    pizza = models.ForeignKey(Pizza, null=True, blank=True, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drinks, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}"

    def get_item_name(self):
        if self.pizza:
            return self.pizza.name
        return self.drink.name
    
    @property
    def total(self):
        if self.drink:
            return self.drink.price * self.quantity
        if self.pizza:
            return self.pizza.price * self.quantity
        return 0
    
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def total_cost(self):
        return sum(item.price for item in self.items.all())

class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    drink = models.ForeignKey(Drinks, null=True, blank=True, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.drink if self.drink else self.pizza}"    
    
