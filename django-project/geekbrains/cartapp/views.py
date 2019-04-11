from django.shortcuts import render, \
    get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

from cartapp.models import ShopCart
from mainapp.models import Products


@login_required
def show(request):
    title = 'Все товары | Корзина'
    cart = ShopCart.objects.select_related(
        'product'
    ).filter(user=request.user).all()
    return render(request, 'cartapp/cart.html',
                  {'title': title,
                   'cart': cart, })


@login_required
def add(request, pk):
    product = get_object_or_404(Products, pk=pk)
    cart = ShopCart.objects.filter(
        user=request.user,
        product=product
    ).first()
    if not cart:
        cart = ShopCart(user=request.user,
                        product=product)
    cart.quantity += 1
    cart.save()

    if request.META.get('HTTP_REFERER', None) is not None and \
            request.META.get('HTTP_REFERER').startswith(settings.LOGIN_URL):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(reverse('products:detail', args=[pk]))


@login_required
def delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    cart = ShopCart.objects.filter(
        user=request.user,
        product=product
    ).first()
    if not cart:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if cart.quantity <= 1:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()

    if request.META.get('HTTP_REFERER', None) is not None and \
            request.META.get('HTTP_REFERER').startswith(settings.LOGIN_URL):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(reverse('cart:index'))


@login_required
def update(request, pk, value):
    product = get_object_or_404(Products, pk=pk)
    cart = ShopCart.objects.filter(
        user=request.user,
        product=product
    ).first()
    if not cart:
        return HttpResponseBadRequest('cart object does not defined')

    if value:
        cart.quantity = value
        cart.save()
    else:
        cart.delete()

    if request.is_ajax():
        cart = ShopCart.objects.select_related(
            'product'
        ).filter(user=request.user).all()
        result = render_to_string('cartapp/include/cart_tbody.html', {'cart': cart, })
        return JsonResponse({'result': result})

    return HttpResponse('successful')
