from pydoc import describe
from django.db import models

# Create your models here.
class Course(models.Model):
    describe = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    review = models.CharField(max_length=255)
