from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.html import strip_tags
import datetime

from .models import Product
from .forms import ProductForm


# ========== MAIN PAGE ==========

@login_required(login_url='/login/')
def show_main(request):
    """Menampilkan halaman utama berisi daftar produk."""
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        products = Product.objects.all().order_by("-id")
    elif filter_type == "my":
        products = Product.objects.filter(user=request.user).order_by("-id")
    else:
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


# ========== AUTH ==========

def register(request):
    """Halaman registrasi pengguna."""
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("main:login")
    return render(request, "register.html", {"form": form})


def login_user(request):
    """Halaman login pengguna."""
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie("last_login", str(datetime.datetime.now()))
        return response
    return render(request, "login.html", {"form": form})


def logout_user(request):
    """Logout pengguna."""
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response


# ========== CRUD PRODUCT ==========

@login_required(login_url='/login/')
def create_product(request):
    """Menambah produk baru."""
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return redirect("main:show_main")
    return render(request, "main/create_product.html", {"form": form})


@login_required(login_url='/login/')
def edit_product(request, pk):
    """Mengedit produk."""
    product = get_object_or_404(Product, pk=pk, user=request.user)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produk berhasil diperbarui.")
        return redirect("main:product_detail", pk=product.pk)
    return render(request, "main/create_product.html", {"form": form, "is_edit": True, "product": product})


@login_required(login_url='/login/')
def delete_product(request, pk):
    """Menghapus produk."""
    product = get_object_or_404(Product, pk=pk, user=request.user)
    name = product.name
    product.delete()
    messages.success(request, f"Produk '{name}' berhasil dihapus.")
    return redirect("main:show_main")


@login_required(login_url='/login/')
def product_detail(request, pk):
    """Menampilkan detail produk."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "main/product_detail.html", {"product": product})


# ========== SERIALIZER (XML & JSON) ==========

def show_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type="application/xml")


def show_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type="application/json")


def show_xml_by_id(request, pk):
    data = serializers.serialize("xml", Product.objects.filter(pk=pk))
    return HttpResponse(data, content_type="application/xml")


def show_json_by_id(request, pk):
    data = serializers.serialize("json", Product.objects.filter(pk=pk))
    return HttpResponse(data, content_type="application/json")


# ========== API ENDPOINTS (AJAX) ==========

def product_to_dict(p):
    return {
        "id": str(p.id),
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "thumbnail": p.thumbnail,
        "category": p.category,
        "is_featured": p.is_featured,
        "stock": p.stock,
        "brand": p.brand,
        "rating": p.rating,
    }


@require_http_methods(["GET"])
def api_products_list(request):
    qs = Product.objects.all().order_by("-id")
    data = [product_to_dict(p) for p in qs]
    return JsonResponse(data, safe=False)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def api_product_create(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return JsonResponse({"status": "ok", "id": str(obj.id)})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def api_product_update(request, pk):
    obj = get_object_or_404(Product, pk=pk, user=request.user)
    form = ProductForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def api_product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk, user=request.user)
    obj.delete()
    return JsonResponse({"status": "ok"})


@require_http_methods(["POST"])
def login_ajax(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return JsonResponse({
            "status": "ok",
            "message": "Logged in",
            "redirect": reverse("main:show_main")
        })
    return JsonResponse({
        "status": "error",
        "errors": form.errors,
        "message": "Invalid credentials"
    }, status=400)


@require_http_methods(["POST"])
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "status": "ok",
            "message": "Registered",
            "redirect": reverse("main:login")
        })
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)
