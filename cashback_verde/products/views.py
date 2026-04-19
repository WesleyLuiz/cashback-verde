from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def create_product(request):
    if request.user.role != 'seller':
        return HttpResponseForbidden("Apenas vendedores podem cadastrar produtos.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Produto cadastrado com sucesso.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'products/create_product.html', {'form': form})
