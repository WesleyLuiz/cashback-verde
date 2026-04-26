from django.contrib import admin
from django import forms

from accounts.models import User
from .models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_seller(self):
        seller = self.cleaned_data.get('seller')

        if seller is None:
            raise forms.ValidationError('Selecione um vendedor para cadastrar o produto.')

        if seller.role != User.SELLER:
            raise forms.ValidationError('O usuário selecionado precisa ter o perfil Vendedor.')

        return seller


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'name',
        'seller',
        'item_type',
        'category',
        'city',
        'price',
        'cashback_percentage',
    )
    list_filter = ('item_type', 'category', 'city', 'seller')
    search_fields = ('name', 'description', 'seller__username', 'seller__email')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'seller':
            kwargs['queryset'] = User.objects.filter(role=User.SELLER)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
