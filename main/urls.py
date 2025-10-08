from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),

    # JSON list & detail (untuk fetch)
    path("json/", views.api_products_list, name="show_json"),
    path("json/<int:pk>/", views.api_product_by_id, name="show_json_by_id"), 

    # AJAX CRUD
    path("ajax/products/create/", views.api_product_create, name="ajax_product_create"),
    path("ajax/products/<uuid:pk>/update/", views.api_product_update, name="ajax_product_update"),
    path("ajax/products/<uuid:pk>/delete/", views.api_product_delete, name="ajax_product_delete"),

    # AJAX Auth
    path("ajax/login/", views.login_ajax, name="ajax_login"),
    path("ajax/register/", views.register_ajax, name="register_ajax"),
    path("ajax/logout/", views.logout_ajax, name="ajax_logout"),

    # (opsional) halaman klasik
    path("product/<uuid:pk>/", views.product_detail, name="product_detail"),
    path("product/<uuid:pk>/edit/", views.edit_product, name="edit_product"),
    path("product/<uuid:pk>/delete/", views.delete_product, name="delete_product"),

    # legacy
    path("xml/", views.show_xml, name="xml_all"),
    path("json-legacy/", views.show_json, name="json_legacy"),
    path("xml/<uuid:id>/", views.show_xml_by_id, name="xml_by_id"),
    path("json-legacy/<uuid:id>/", views.show_json_by_id, name="json_by_id"),

    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"), 

]
