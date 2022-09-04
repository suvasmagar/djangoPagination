from django_filters.rest_framework import FilterSet
from .models import Cart, Product, CartItem

class ProductFilter(FilterSet):
    class Meta:
        model= Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': [ 'gt', 'lt'],
        }

class CartItemFilter(FilterSet):
    class Meta:
        model = CartItem
        fields = {
            'id' : ['exact'],
            'quantity': ['gt','lt'],
        }