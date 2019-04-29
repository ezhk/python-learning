from cartapp.models import ShopCart


def cart(request):
    cart = []
    if request.user.is_authenticated:
        cart = ShopCart.objects.filter(user=request.user)
    return {'cart': cart}
