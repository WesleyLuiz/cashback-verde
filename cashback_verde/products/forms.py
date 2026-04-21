from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['item_type', 'category', 'city']:
            self.fields[field_name].widget.attrs['class'] = 'form-select'

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['is_sustainable'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'image',
            'item_type',
            'category',
            'city',
            'is_sustainable',
        ]
