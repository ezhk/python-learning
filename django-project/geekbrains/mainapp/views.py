import json

from django.shortcuts import render
from django.http import HttpResponseNotFound

from mainapp.models import Products, ProductCategory, ProductProperty

def main(request):
    return render(request, 'mainapp/index.html')


def products(request, pk=None):
    categories = ProductCategory.objects.all()
    if pk is not None:
        products = Products.objects.filter(category=pk).all()
    else:
        products = Products.objects.all()

    return render(request, 'mainapp/products.html',
                  {
                      'products': products,
                      'categories': categories
                  })

def products_details(request, pk=None):
    if pk is not None:
        HttpResponseNotFound("product ID not found")

    product = Products.objects.get(pk=pk)
    properties = ProductProperty.objects.filter(product=pk).values('name')
    return render(request, 'mainapp/product-detail.html',
                  {'product_description': product,
                   'product_properties': properties})

def contacts(request):
    return render(request, 'mainapp/contacts.html')
