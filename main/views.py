from django.shortcuts import render
from .models import Product

def show_main(request):
    products = Product.objects.all()
    return render(request, "main/index.html", {
        "name": "Febrian Abimanyu Wijanarko",
        "class": "PBP CSGE602022 – 2025/2026",
        "products": products,
    })
