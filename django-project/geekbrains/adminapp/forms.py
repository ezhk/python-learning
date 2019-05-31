from django import forms

from mainapp.models import ProductCategory


class ProductCategoryForm(forms.ModelForm):
    discount = forms.FloatField(label='Discount percent', required=False,
                                min_value=0.0, max_value=99.9, initial=0.0)

    class Meta:
        model = ProductCategory
        fields = '__all__'
