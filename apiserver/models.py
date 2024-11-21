from attr import NOTHING
from django.db import models
from django.contrib.auth.models import AbstractUser
import json


class CusUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=30)
    firstname = models.CharField(max_length=150,unique=False)
    profile_image = models.ImageField(upload_to='profile/',default='profile/default.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','firstname']


    def __str__(self):
        return self.email
    

# class Order(models.Model):
#     user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     order_id = models.CharField(max_length=100,blank=True)
#     razorpay_payment_id = models.CharField(max_length=100,blank=True)
#     paid = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user} Order'

class Explore_menu(models.Model):
    food_name = models.CharField(max_length=250)
    food_image = models.ImageField(upload_to='food_images/')

    def __str__(self):
        return self.food_name


class item_List(models.Model):
    category = models.ForeignKey(Explore_menu, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    description = models.TextField(max_length=250)
    image = models.ImageField(upload_to='itemList/')

    def __str__(self):
            return f'{self.name} ({self.category.food_name if self.category else "No category"})'
    

class CartItem(models.Model):
    item = models.ForeignKey(item_List, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.item.name}--{self.quantity}'


class Cart(models.Model):
    user = models.OneToOneField(CusUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, blank=True, related_name='carts')
    total = models.DecimalField(default=0,decimal_places=2,max_digits=10)

    def __str__(self):
        return f'{self.user.username} Cart'


class Address(models.Model):
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    door = models.CharField(max_length=250)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=10)
    district = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if self.user_id is not None:
            self.user.firstname = self.fullname
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} Address'

class UserOrders(models.Model):
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
    items = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)  # Allow this to be null
    cart_snapshot = models.JSONField(default=dict)  # New field to store cart snapshot
    order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')
    arriveAt = models.DateField()

    def __str__(self):
        return f'{self.user} Order'