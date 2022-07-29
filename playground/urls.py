from django.urls import path
from . import views

urlpatterns = [
    path('', views.showHello, name='says_hello'),
    path('', views.showTemplate, name='says_template'),

]