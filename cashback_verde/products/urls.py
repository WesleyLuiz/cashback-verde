from django.urls import path

from .views import create_product, product_detail, product_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('novo/', create_product, name='product_create'),
    path('<int:pk>/', product_detail, name='product_detail'),
]
