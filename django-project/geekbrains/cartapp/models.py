from django.db import models
from django.conf import settings

from mainapp.models import Products


class ShopCart(models.Model):
    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    created_at = models.DateTimeField(verbose_name='Время добавления товара',
                                      auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.product.quantity} x {self.product.name})"

    @property
    def summary_products_count(self):
        products_count = 0
        for cart_object in ShopCart.objects.filter(user=self.user).all():
            products_count += cart_object.quantity
        return products_count
