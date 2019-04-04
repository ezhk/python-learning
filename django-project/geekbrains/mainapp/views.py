import json

from django.shortcuts import render
from django.http import HttpResponseNotFound

from mainapp.models import Products, \
    ProductCategory, \
    ProductAndProperty


def main(request):
    title = 'Все товары'
    return render(request, 'mainapp/index.html', {'title': title})


def products(request, pk=None):
    title = 'Все товары | Каталог'
    categories = ProductCategory.objects.all()
    if pk is not None:
        products = Products.objects.filter(category=pk).all()
    else:
        products = Products.objects.all()

    return render(request, 'mainapp/products.html',
                  {
                      'title': title,
                      'products': products,
                      'categories': categories
                  })


def products_details(request, pk=None):
    title = 'Все товары | Описание'
    if pk is not None:
        HttpResponseNotFound("product ID not found")

    product = Products.objects.get(pk=pk)
    properties = ProductAndProperty.objects.select_related(
        'property'
    ).filter(product=pk).all()
    return render(request, 'mainapp/product-detail.html',
                  {'title': title,
                   'product_description': product,
                   'product_properties': properties})


def contacts(request):
    title = 'Все товары | Контакты'
    return render(request, 'mainapp/contacts.html',
                  {'title': title})
