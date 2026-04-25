from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            'Informe um nome de usuário e senha válidos. '
            'Lembre-se de que ambos os campos diferenciam letras maiúsculas e minúsculas.'
        ),
        'inactive': 'Esta conta está inativa.',
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite seu nome de usuário',
            'autocomplete': 'username',
        })
        self.fields['username'].error_messages['required'] = 'Informe seu nome de usuário.'

        self.fields['password'].label = 'Senha'
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite sua senha',
            'autocomplete': 'current-password',
        })
        self.fields['password'].error_messages['required'] = 'Informe sua senha.'


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=(
            '<ul>'
            '<li>Sua senha não pode ser muito parecida com suas outras informações pessoais.</li>'
            '<li>Sua senha precisa conter pelo menos 8 caracteres.</li>'
            '<li>Sua senha não pode ser uma senha muito comum.</li>'
            '<li>Sua senha não pode ser inteiramente numérica.</li>'
            '</ul>'
        ),
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Digite a mesma senha novamente para confirmação.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages['required'] = 'Este campo é obrigatório.'

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Escolha um nome de usuário',
            'autocomplete': 'username',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite seu e-mail',
            'autocomplete': 'email',
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-select form-select-lg',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Crie uma senha',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirme sua senha',
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'role': 'Perfil',
        }
        help_texts = {
            'username': (
                'Obrigatório. Use até 150 caracteres. '
                'Letras, números e os símbolos @/./+/-/_ são permitidos.'
            ),
        }
