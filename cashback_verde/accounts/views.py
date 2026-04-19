from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


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
