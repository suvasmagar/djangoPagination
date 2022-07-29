from django.urls import path
from . import views
from rest_framework_nested import routers
# from pprint import pprint
 
# DefaultRouter helps with 2 additional features
# we get link to the other links available 
# .json format with .json extension


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSets, basename='product-review')


urlpatterns = router.urls + product_router.urls
#     path('',include(routers.urls))  
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetails.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection_detail'),
#     path('collections/', views.CollectionList.as_view(), name='collection_list'),
