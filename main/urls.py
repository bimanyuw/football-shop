from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add/', views.create_product, name='create_product'),
    path('detail/<uuid:pk>/', views.product_detail, name='product_detail'),
    path('edit/<uuid:pk>/', views.edit_product, name='edit_product'),
    path('delete/<uuid:pk>/', views.delete_product, name='delete_product'),
    # API
    path('api/products/', views.api_products_list, name='api_products_list'),
    path('api/products/create/', views.api_product_create, name='api_product_create'),
    path('api/products/<uuid:pk>/update/', views.api_product_update, name='api_product_update'),
    path('api/products/<uuid:pk>/delete/', views.api_product_delete, name='api_product_delete'),
]
