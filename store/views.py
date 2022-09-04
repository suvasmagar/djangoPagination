from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from store.pagination import DefaultPagination
from .models import Collection, OrderItem, Product, Review, Cart, CartItem
from .serializers import AddCartItemSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, UpdateCartItemSeriailizer
from .filters import ProductFilter, CartItemFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter , OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = [ 'unit_price', 'last_update']

    #queryset = Product.objects.all()
    # since we cannot use filter on queryset so we override the function
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset
        # the self.request.query_params reads the value of collection id form the url as request query



    # def get_serializer_class(self):
    #     return {'request': self.request}

# by doing this the delete button also appeared while listing all
# product details and for so we need to overried destroy function 
# not the delete function, which was used when we passed retrieveupdatedeleteapiview module

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitem_set.count() > 0:
    #         return Response({'error': 'Product cannot be deleted becuase it is associated with an order itam'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response({'sucessfully deleted'},status = status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted becuase it is associated with an order itam'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted becuase it is associated with an Product item'},
                status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response(
    #             {'error': 'Collection cannot be deleted becuase it is associated with an Product item'},
    #             status = status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response({'sucessfully deleted'},status = status.HTTP_204_NO_CONTENT)


class ReviewViewSets(ModelViewSet):
    serializer_class = ReviewSerializer

    # queryset = Review.objects.all()
    # all reviews are displayed no matter what the product id is, so we use filter method
    # since queryset doesnt allow us to access self inorder to access url product pk so we overried the get_queryset
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])


    # after removing product id which is the foreign key to review model
    # we have to create auto reader for product id where we are giving review
    # for that we need to override the getserializer_context class
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    # keyword id and primary key
    # a url has two parameters a productpk and pk of url 

# Create your views here.
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}

    # def get(self, request):
    #     products = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(products, many=True, context={'request': request})
    #     return Response(serializer.data)
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetails(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Product cannot be deleted becuase it is associated with an order itam'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()

# using RetrieveUPdateDestroyAPIView all functions within one
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Product cannot be deleted becuase it is associated with an order itam'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({'sucessfully deleted'},status = status.HTTP_204_NO_CONTENT)



# class CollectionList(ListCreateAPIView):
#      # add readonly to productcount
#     # queryset =Collection.objects.annotate(
#     #     products_count = count('Product')).all()
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer


# @api_view(['GET', 'PUT'])
# def collection_list(request):
#     if request.method == 'GET':
#         collections = Collection.objects.annotate(product_count=count('Product')).all()
#         # collections = Collection.objects.all()
#         serializer = CollectionSerializer(collections, many=True, context={'request': request})
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
    # queryset = Collection.objects.annotate(
    #     product_count = count('products'))
    # queryset = Collection.objects.all()
    # serializer_class = CollectionSerializer
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response(
    #             {'error': 'Collection cannot be deleted becuase it is associated with an Product item'},
    #             status = status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response({'sucessfully deleted'},status = status.HTTP_204_NO_CONTENT)


# api normal way
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         # Collection.objects.annotate(
#         #     product_count=count('products')
#         # ), 
#         Collection,
#         pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         # httpstatuses.com go for this websites inorder to solve unable to dleteion of product 
#         # where they are included as foreign key to another class
#         if collection.products.count() > 0:
#             return Response(
#                 {'error': 'Collection cannot be deleted becuase it is associated with an Product item'},
#                 status = status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response({'sucessfully deleted'},status = status.HTTP_204_NO_CONTENT)

# ModelViewSet class provides all operation create, update, list, delete
# since we dnot have list method to implement so we dont use ModelViewSet
# instead we will use custom viewset
class CartViewSet(CreateModelMixin,
                RetrieveModelMixin,
                DestroyModelMixin, 
                GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=kwargs['pk'])
        if cart.items.count() > 0:
            return Response(
                {'error': 'cart cannot be deleted becuase it is associated with an Product item'},
                status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # serializer_class = UpdateCartItemSeriailizer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request == 'PATCH':
            return UpdateCartItemSeriailizer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id =self.kwargs['cart_pk'])
    
    # filter_backends = [DjangoFilterBackend, SearchFilter , OrderingFilter]
    # filterset_class = CartItemFilter
    # pagination_class = DefaultPagination
    # search_fields = ['cart']
    # ordering_fields = [ 'quantity']