from django.urls import path
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm
from .views import register

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            authentication_form=CustomAuthenticationForm,
            template_name='registration/login.html',
        ),
        name='login',
    ),
    path('register/', register, name='register'),
]
