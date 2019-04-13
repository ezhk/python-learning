from django import template

register = template.Library()


@register.filter
def explain_gender(username):
    return username.get_gender_display()
