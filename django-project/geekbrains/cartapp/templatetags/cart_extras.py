from django import template

register = template.Library()


@register.filter
def summary_price(cart):
    summary_price = 0
    for cart_id in cart:
        summary_price += cart_id.quantity * cart_id.product.price
    return summary_price


@register.filter
def summary_count(cart):
    summary_count = 0
    for card_id in cart:
        summary_count += card_id.quantity
    return summary_count
