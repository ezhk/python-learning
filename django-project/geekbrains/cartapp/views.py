from django.shortcuts import render, \
    get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from cartapp.models import ShopCart
from mainapp.models import Products


@login_required(login_url='/auth/')
def show(request):
    title = 'Все товары | Корзина'
    cart = ShopCart.objects.select_related(
        'product'
    ).filter(user=request.user).all()
    return render(request, 'cartapp/cart.html',
                  {'title': title,
                   'cart': cart, })


@login_required(login_url='/auth/')
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/auth/')
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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
