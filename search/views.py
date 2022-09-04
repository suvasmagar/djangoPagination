from django.shortcuts import render
from .models import Document
from rest_framework.viewsets import ModelViewSet, GenericViewSet

# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Document.objects.all()
    search_fields = ['describe', 'title', 'review']