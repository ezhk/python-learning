from django import forms

from mainapp.models import Products
from orderapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Цена', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_initial_for_field(self, field, field_name):
        if field_name == 'product':
            field.queryset = Products.objects.filter(is_active=True).all()
        return super(OrderItemForm, self).get_initial_for_field(field, field_name)
