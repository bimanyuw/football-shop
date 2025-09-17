from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from .models import Product
from .forms import ProductForm

def show_main(request):
    products = Product.objects.all().order_by("-id")
    context = {
        "name": "Febrian Abimanyu Wijanarko",
        "npm": "2406397984",
        "class": "PBP D",
        "products": products,
    }
    return render(request, "main/index.html", context)

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():        
            form.save()
            return redirect("show_main")
    else:
        form = ProductForm()
    return render(request, "main/create_product.html", {"form": form})

def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "main/product_detail.html", {"product": product})

def show_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type="application/json")

def show_xml_by_id(request, id: int):
    data = serializers.serialize("xml", Product.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/xml")

def show_json_by_id(request, id: int):
    data = serializers.serialize("json", Product.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/json")
