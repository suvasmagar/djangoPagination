import re
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def showHello(request):
    return HttpResponse("Hello World!")

def showTemplate(request):
        return HttpResponse("Hello World66!")

   # return render(request, 'index.html')
