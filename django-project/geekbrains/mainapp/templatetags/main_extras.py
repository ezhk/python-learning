from django import template

register = template.Library()


@register.filter
def is_discount(product, pk):
    return pk in product.values_list('pk', flat=True)
