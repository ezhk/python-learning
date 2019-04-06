from django import template
from mainapp.models import Products

register = template.Library()


@register.filter
def summary_price(cart):
    summary_price = 0
    for card_id in cart:
        summary_price += card_id.quantity * card_id.product.price
    return summary_price


@register.filter
def summary_count(cart):
    summary_count = 0
    for card_id in cart:
        summary_count += card_id.quantity
    return summary_count
