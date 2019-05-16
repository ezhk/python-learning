from django.db import models

from django.conf import settings
from mainapp.models import Products


class Order(models.Model):
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    ORDER_STATUS_NEW = 'N'
    ORDER_STATUS_PROCESSING = 'PRC'
    ORDER_STATUS_PREPARED = 'PRP'
    ORDER_STATUS_PAID = 'PD'
    ORDER_STATUS_READY = 'R'
    ORDER_STATUS_CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (ORDER_STATUS_NEW, 'Новый'),
        (ORDER_STATUS_PROCESSING, 'Формируется'),
        (ORDER_STATUS_PREPARED, 'Подготовлен'),
        (ORDER_STATUS_PAID, 'Оплачен'),
        (ORDER_STATUS_READY, 'Готов к выдаче'),
        (ORDER_STATUS_CANCEL, 'Отменен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=3,
                              choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_NEW)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    def delete(self, using=None, keep_parents=False):
        for item in self.order.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        return super().delete(using, keep_parents)


class OrderItemQuerySet(models.QuerySet):
    def delete(self):
        for order_item_object in self:
            order_item_object.product.quantity += order_item_object.quantity
            order_item_object.product.save()
        return super().delete()


class OrderItem(models.Model):
    object = OrderItemQuerySet.as_manager()
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='product',
                                verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()

        return super().delete(using, keep_parents)
