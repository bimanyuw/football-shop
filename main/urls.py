# main/urls.py
from django.urls import path
from . import views  

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("add/", views.create_product, name="create_product"),
    path("detail/<uuid:pk>/", views.product_detail, name="product_detail"),
    path("xml/<uuid:id>/", views.show_xml_by_id, name="show_xml_by_id"),
    path("json/<uuid:id>/", views.show_json_by_id, name="show_json_by_id"),
    path("delete/<uuid:pk>/", views.delete_product, name="delete_product"),
    path("edit/<uuid:pk>/", views.edit_product, name="edit_product"),
]

