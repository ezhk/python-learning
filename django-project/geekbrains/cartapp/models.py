from django.db import models
from django.conf import settings

from mainapp.models import Products


class ShopCartQuerySet(models.QuerySet):
    def delete(self):
        for cart_object in self:
            cart_object.product.quantity += cart_object.quantity
            cart_object.product.save()
        return super().delete()


class ShopCart(models.Model):
    object = ShopCartQuerySet.as_manager()
    objects = models.Manager()

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

    def save(self, *args, **kwargs):
        if self.pk:
            changed_quantity = self.quantity - self.__class__.objects.get(pk=self.pk).quantity
            self.product.quantity -= changed_quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()

        return super().delete(using, keep_parents)
