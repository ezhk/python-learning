from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

from cartapp.models import ShopCart
from orderapp.models import OrderItem


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=ShopCart)
def pre_save_update_product_quantity(sender, instance, **kwargs):
    if instance.pk:
        changed_quantity = instance.quantity - instance.__class__.objects.get(pk=instance.pk).quantity
        instance.product.quantity -= changed_quantity
    else:
        instance.product.quantity -= instance.quantity
    return instance.product.save()


@receiver(post_delete, sender=OrderItem)
@receiver(post_delete, sender=ShopCart)
def post_delete_update_product_quantity(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    return instance.product.save()
