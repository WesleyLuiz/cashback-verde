from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from products.models import Product


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso. Bem-vindo(a)!')
            return redirect('home')
        messages.error(request, 'Não foi possível criar a conta. Verifique os campos abaixo.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


@login_required
def profile(request):
    seller_products = Product.objects.none()

    if request.user.role == 'seller':
        seller_products = request.user.products.order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'seller_products': seller_products,
    })
