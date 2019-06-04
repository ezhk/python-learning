from django.dispatch import receiver
from django.db.models.signals import pre_save

from geekbrains import settings
from mainapp.models import ProductCategory


def db_profile(queries):
    for q in queries:
        print('\t', q.get('sql'))


@receiver(pre_save, sender=ProductCategory)
def pre_save_update_category_active(sender, instance, **kwargs):
    if not instance.pk:
        return
    instance.products_set.update(is_active=instance.is_active)

    if settings.DEBUG:
        from django.db import connection
        db_profile(connection.queries)
