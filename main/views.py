# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_protect
import datetime

from .models import Product
from .forms import ProductForm


# =======================
# Page container (AJAX)
# =======================
@login_required(login_url='/login/')
def show_main(request):
    """Render halaman utama; list produk di-load via JS (fetch JSON)."""
    return render(request, "main/index.html", {
        "name": request.user.username,
        "npm": "2406397984",
        "class": "PBP D",
        "last_login": request.COOKIES.get("last_login", "Never"),
    })


# =======================
# Serializer helper
# =======================
def product_to_dict(p: Product):
    return {
        "id": str(p.id),
        "name": p.name,
        "price": p.price,
        "description": p.description or "",
        "thumbnail": getattr(p, "thumbnail", "") or "",
        "category": getattr(p, "category", "") or "",
        "is_featured": getattr(p, "is_featured", False),
        "stock": getattr(p, "stock", 0),
        "brand": getattr(p, "brand", "") or "",
        "rating": getattr(p, "rating", 0),
        "user_id": p.user_id,
        "created_at": getattr(p, "created_at", None).isoformat() if getattr(p, "created_at", None) else None,
    }


# =======================
# JSON list & detail (Tutorial: show_json & show_json_by_id)
# =======================
@require_http_methods(["GET"])
def api_products_list(request):
    """Return list product dalam JSON (dipakai index via fetch)."""
    qs = Product.objects.all().order_by("-id")
    data = [product_to_dict(p) for p in qs]
    # sesuai tutorial: kembalikan LIST langsung
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def api_product_by_id(request, pk):
    """Return detail 1 product (dipakai halaman detail AJAX, kalau diperlukan)."""
    try:
        p = Product.objects.select_related("user").get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"detail": "Not found"}, status=404)
    data = product_to_dict(p)
    data["user_username"] = p.user.username if p.user_id else None
    return JsonResponse(data)


# =======================
# AJAX CRUD (Create/Update/Delete) — JSON only
# =======================
@login_required(login_url='/login/')
@require_http_methods(["POST"])
def api_product_create(request):
    # XSS defense (server-side), sesuai tutorial: strip_tags
    post = request.POST.copy()
    if "name" in post: post["name"] = strip_tags(post["name"])
    if "description" in post: post["description"] = strip_tags(post["description"])

    form = ProductForm(post)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return JsonResponse({"ok": True, "msg": "Created", "data": product_to_dict(obj)}, status=201)
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@login_required(login_url='/login/')
@require_http_methods(["POST"])
def api_product_update(request, pk):
    obj = get_object_or_404(Product, pk=pk, user=request.user)

    post = request.POST.copy()
    if "name" in post: post["name"] = strip_tags(post["name"])
    if "description" in post: post["description"] = strip_tags(post["description"])

    form = ProductForm(post, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"ok": True, "msg": "Updated", "data": product_to_dict(obj)})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@login_required(login_url='/login/')
@require_http_methods(["POST"])
def api_product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk, user=request.user)
    obj.delete()
    return JsonResponse({"ok": True, "msg": "Deleted"})


# =======================
# Auth (AJAX)
# =======================
@require_http_methods(["POST"])
def login_ajax(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        resp = JsonResponse({
            "ok": True,
            "msg": "Logged in",
            "redirect": reverse("main:show_main")
        })
        resp.set_cookie("last_login", str(datetime.datetime.now()))
        return resp
    return JsonResponse({"ok": False, "errors": form.errors, "msg": "Invalid credentials"}, status=400)

@require_http_methods(["POST"])
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "ok": True,
            "msg": "Registered",
            "redirect": reverse("main:show_main"),
        })
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@login_required(login_url='/login/')
@require_http_methods(["POST"])
def logout_ajax(request):
    logout(request)
    resp = JsonResponse({"ok": True, "msg": "Logged out"})
    resp.delete_cookie("last_login")
    return resp


# =======================
# (Opsional) Halaman klasik yang masih kamu pakai
# =======================
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
        "form": form, "is_edit": True, "product": product
    })

@login_required(login_url='/login/')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "main/product_detail.html", {"product": product})

@login_required(login_url='/login/')
@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    name = product.name
    product.delete()
    messages.success(request, f"Produk '{name}' berhasil dihapus.")
    return redirect('main:show_main')


# =======================
# Legacy serializer (tugas sebelumnya)
# =======================
def show_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type="application/json")

def show_xml_by_id(request, id):
    data = serializers.serialize("xml", Product.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/xml")

def show_json_by_id(request, id):
    data = serializers.serialize("json", Product.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/json")


# =======================
# Auth (render biasa sebagai fallback)
# =======================
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("main:login")
    return render(request, "register.html", {"form": form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie("last_login", str(datetime.datetime.now()))
        return response
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
