from django.db import models
from django.conf import settings

from mainapp.models import Products


class ShopCart(models.Model):
    class Meta:
        unique_together = ('user', 'product')

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    created_at = models.DateTimeField(verbose_name='Время добавления товара',
                                      auto_now_add=True)
