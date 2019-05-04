from django import template

register = template.Library()


@register.filter
def is_discount(product, pk):
    return pk in product.values_list('pk', flat=True)


@register.filter
def products_quantity(cart):
    return sum([product.quantity for product in cart])
