from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
import datetime  

from .models import Product
from .forms import ProductForm

@login_required(login_url='/login/')
def show_main(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        products = Product.objects.all().order_by("-id")
    elif filter_type == "my":
        products = Product.objects.filter(user=request.user).order_by("-id")
    else:
        # kategori (case-insensitive)
        products = Product.objects.filter(category__iexact=filter_type).order_by("-id")

    context = {
        "name": request.user.username,
        "npm": "2406397984",
        "class": "PBP D",
        "products": products,
        "last_login": request.COOKIES.get("last_login", "Never"),
        "filter_type": filter_type,
    }
    return render(request, "main/index.html", context)


@login_required(login_url='/login/')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("main:show_main")
    else:
        form = ProductForm()
    return render(request, "main/create_product.html", {"form": form})

@login_required(login_url='/login/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil diperbarui.")
            return redirect("main:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "main/create_product.html", {
        "form": form,
        "is_edit": True,
        "product": product,
    })

@login_required(login_url='/login/')
def product_detail(request, pk):
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


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return HttpResponseRedirect(reverse('main:login'))
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login/')
@require_POST
def delete_product(request, pk):
    # Pastikan hanya pemilik produk yang bisa menghapus
    product = get_object_or_404(Product, pk=pk, user=request.user)
    name = product.name
    product.delete()
    messages.success(request, f"Produk '{name}' berhasil dihapus.")
    return redirect('main:show_main')
