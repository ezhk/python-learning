from django import forms

from product.models import Product, Provider


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
