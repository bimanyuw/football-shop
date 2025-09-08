from django.shortcuts import render
from .models import Product

def show_main(request):
    products = Product.objects.all()  # ambil semua produk dari DB
    context = {
        "npm": "2406397984",
        "name": "Febrian Abimanyu Wijanarko",
        "class": "PBP CSGE602022",
        "products": products,
    }
    return render(request, "main/index.html", context)
