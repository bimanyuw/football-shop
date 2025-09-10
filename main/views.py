# main/views.py
from django.shortcuts import render
from .models import Product

def home(request):  
    products = Product.objects.all()
    context = {
        "name": "Febrian Abimanyu Wijanarko",
        "npm": "2406397984",     
        "class": "PBP D",        
        "products": products,
    }
    return render(request, "index.html", context)
