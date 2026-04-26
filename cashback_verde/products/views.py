from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.all()
    selected_item_type = request.GET.get('item_type', '')
    selected_category = request.GET.get('category', '')
    selected_city = request.GET.get('city', '')

    if selected_item_type:
        products = products.filter(item_type=selected_item_type)

    if selected_category:
        selected_categories = [
            category.strip()
            for category in selected_category.split(',')
            if category.strip()
        ]
        products = products.filter(category__in=selected_categories)

    if selected_city:
        products = products.filter(city=selected_city)

    context = {
        'products': products,
        'item_type_choices': Product.ITEM_TYPE_CHOICES,
        'category_choices': Product.CATEGORY_CHOICES,
        'city_choices': Product.CITY_CHOICES,
        'selected_item_type': selected_item_type,
        'selected_category': selected_category,
        'selected_city': selected_city,
    }
    return render(request, 'products/product_list.html', context)


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


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.role != 'seller' or product.seller != request.user:
        return HttpResponseForbidden("Apenas o vendedor do anúncio pode editar este produto.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/create_product.html', {
        'form': form,
        'product': product,
        'page_title': 'Editar anúncio',
        'page_description': 'Atualize as informações do seu produto ou serviço.',
        'submit_label': 'Salvar alterações',
    })


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.role != 'seller' or product.seller != request.user:
        return HttpResponseForbidden("Apenas o vendedor do anúncio pode remover este produto.")

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto removido com sucesso.')
        return redirect('product_list')

    return render(request, 'products/delete_product.html', {'product': product})
