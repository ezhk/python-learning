import json

from django.conf import settings
from django.shortcuts import render

# Create your views here.


def main(request):
    return render(request, 'mainapp/index.html')


def products(request, product_name=None):
    if product_name is not None:
        return render(request, 'mainapp/products/%s.html' % product_name)

    with open(settings.PRODUCT_CATEGORIES_MENU, 'r') as fh:
        product_categories = json.load(fh)
    return render(request, 'mainapp/products.html', {'categories': product_categories})


def contacts(request):
    return render(request, 'mainapp/contacts.html')
