from itertools import product
from pyexpat import model
from rest_framework import serializers
from .models import Collection, Product, Review
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'tittle']
        # product_count = serializers.IntegerField(read_only = True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'invetory' ,'price_with_tax','collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calc_tax')
    #collection = CollectionSerializer()

    def calc_tax(self, product: Product):
        return product.unit_price * Decimal(1.05)
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password do not match')
    #     return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

        # we deleted the product field inorder to auto assign its value from
        # nested routing from product to the review the specific product id
        # override create method to cerate review
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)