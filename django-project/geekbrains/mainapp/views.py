import sys

from django.shortcuts import render, \
    get_object_or_404
from django.http import HttpResponseNotFound

from mainapp.models import Products, \
    ProductCategory, \
    ProductAndProperty, \
    FeedBack

from mainapp.forms import FeedBackForm


def main(request):
    title = 'Все товары'
    return render(request, 'mainapp/index.html', {'title': title})


def products(request, pk=None):
    def hot_deals():
        """Logic hot deals: get first random element"""
        return Products.objects.order_by('?').all()[:1]

    title = 'Все товары | Каталог'
    categories = ProductCategory.objects.all()

    discount_products = hot_deals()
    if pk is None:
        # welcome products page — hot deal will be here
        products = discount_products
    elif not pk:
        # 0 os "All" category
        products = Products.objects.all()
    elif get_object_or_404(ProductCategory, pk=pk):
        products = Products.objects.filter(category=pk).all()

    return render(request, 'mainapp/products.html',
                  {
                      'title': title,
                      'products': products,
                      'discount_products': discount_products,
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

    feedback_form = FeedBackForm(request.POST)
    if request.method == 'POST':
        if feedback_form.is_valid():
            FeedBack(
                username=feedback_form.data.get('username', None),
                email=feedback_form.data.get('email'),
                subject=feedback_form.data.get('subject', None),
                body=feedback_form.data.get('body')
            ).save()
    elif request.user.is_authenticated and request.user.email:
        feedback_form = FeedBackForm({'email': request.user.email})

    return render(request, 'mainapp/contacts.html',
                  {'title': title,
                   'feedback_form': feedback_form})


def page404(request, exception):
    paths = [arg.get('path')
             for arg in exception.args if arg.get('path', None) is not None]
    return render(request, 'mainapp/page404.html',
                  context={'exception_path': paths}, status=404)


def page500(request):
    (_type, value, traceback) = sys.exc_info()
    exception = value
    if hasattr(value, 'backend'):
        exception = value.backend
    return render(request, 'mainapp/page500.html',
                  context={'exception': exception}, status=500)
