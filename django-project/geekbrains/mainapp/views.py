import sys

from django.core.cache import cache
from django.shortcuts import render, \
    get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.template.loader import render_to_string
from django.utils.crypto import random

from mainapp.models import Products, \
    ProductCategory, \
    ProductAndProperty, \
    FeedBack

from mainapp.forms import FeedBackForm


def main(request):
    title = 'Все товары'
    return render(request, 'mainapp/index.html', {'title': title})


def products(request, pk=None):
    def get_menu_categories():
        key = 'menu-categories'
        cached_value = cache.get(key, None)
        if cached_value is not None:
            return cached_value
        cache.set(key,
                  ProductCategory.objects.filter(
                      is_active=True
                  ).all(),
                  timeout=1800)
        return cache.get(key)

    def get_all_products():
        key = 'all-products'
        cached_value = cache.get(key, None)
        if cached_value is not None:
            return cached_value
        cache.set(key,
                  Products.objects.filter(
                      is_active=True,
                      category__is_active=True
                  ).select_related('category').all(),
                  timeout=120)
        return cache.get(key)

    def hot_deals():
        """Logic hot deals: get first random element"""
        key = 'products-hot-deals'
        cached_value = cache.get(key, None)
        if cached_value is not None:
            return cached_value

        _products = get_all_products()
        if not _products.count():
            return Products.objects.none()

        cache.set(key,
                  [random.choice(_products)],
                  timeout=120)
        return cache.get(key)
        # return Products.objects.filter(is_active=True,
        #                                category__is_active=True).order_by('?').all()[:1]

    title = 'Все товары | Каталог'
    # categories = ProductCategory.objects.filter(is_active=True).all()

    discount_products = hot_deals()
    if pk is None:
        # welcome products page — hot deal will be here
        products = discount_products
    elif not pk:
        # 0 as "All" category
        products = get_all_products()
    elif get_object_or_404(ProductCategory, pk=pk):
        products = get_all_products().filter(category=pk)

    context = {
        'title': title,
        'products': products,
        'discount_products': discount_products,
        'categories': get_menu_categories(),
    }
    if request.is_ajax():
        return JsonResponse({'result': render_to_string('mainapp/include/product-list.html',
                                                        request=request,
                                                        context=context)})

    return render(request, 'mainapp/products.html',
                  context=context)


def products_details(request, pk=None):
    def get_product(pk):
        key = f'product-{pk}'
        cached_value = cache.get(key, None)
        if cached_value is not None:
            return cached_value
        cache.set(key,
                  get_object_or_404(Products, pk=pk),
                  timeout=3600)
        return cache.get(key)

    title = 'Все товары | Описание'
    if pk is None:
        HttpResponseNotFound("product ID not found")

    product = get_product(pk)
    properties = ProductAndProperty.objects.select_related(
        'property'
    ).filter(product=pk).all()

    if request.is_ajax():
        return JsonResponse({'name': product.name,
                             'price': product.price,
                             'quantity': product.quantity})
        # return HttpResponse(serializers.serialize("json", (product,),
        #                                           fields=('name', 'price', 'quantity',)))

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
    # if hasattr(exception.args, 'get'):
    #     paths = [arg.get('path')
    #              for arg in exception.args if arg.get('path', None) is not None]
    return render(request, 'mainapp/page404.html',
                  context={'exception': exception.args}, status=404)


def page500(request):
    (_type, value, traceback) = sys.exc_info()
    exception = value
    if hasattr(value, 'backend'):
        exception = value.backend
    return render(request, 'mainapp/page500.html',
                  context={'exception': exception}, status=500)
