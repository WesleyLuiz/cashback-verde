from django.urls import path

from .views import (
    create_product,
    delete_product,
    product_detail,
    product_list,
    update_product,
)

urlpatterns = [
    path('', product_list, name='product_list'),
    path('novo/', create_product, name='product_create'),
    path('<int:pk>/editar/', update_product, name='product_update'),
    path('<int:pk>/remover/', delete_product, name='product_delete'),
    path('<int:pk>/', product_detail, name='product_detail'),
]
