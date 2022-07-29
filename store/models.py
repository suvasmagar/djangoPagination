from http.client import PAYMENT_REQUIRED
from itertools import product
from operator import truediv
from pyexpat import model
from tkinter import CASCADE
from django.db import models

#promotion - product many to many relationship
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discont = models.FloatField()

# Create your models here.
class Collection(models.Model):
    tittle = models.CharField(max_length=255)
    feature_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL, 
        null= True,
        related_name='+')

    def __str__(self):
        return self.tittle
    
    class Meta:
        ordering = ['tittle']

class Product(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    invetory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    promotion = models.ManyToManyField(Promotion, blank=True)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICE, default= MEMBERSHIP_BRONZE)

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_REQUIRED = [
        (PAYMENT_PENDING, 'pending'),
        (PAYMENT_COMPLETE, 'complete'),
        (PAYMENT_FAILED, 'failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, 
        choices=PAYMENT_REQUIRED,
        default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    #one to one relation
    '''
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE,
         primary_key=True)
    '''
    #one to many realtionship
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
    )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, 
        on_delete=models.PROTECT)
    quantatiy = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)