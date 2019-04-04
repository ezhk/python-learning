import os

from django.conf import settings
from mainapp.models import ProductCategory, \
                           Products,        \
                           Properties,      \
                           ProductAndProperty
from django.core.management.base import BaseCommand
from django.core import serializers





class Command(BaseCommand):
    def handle(self, *args, **options):
        os.makedirs(settings.DATA_DUMP_DIR, exist_ok=True)
        for database in ProductCategory, Products, Properties, ProductAndProperty:
            try:
                obj = serializers.serialize("json", database.objects.all())
                with open(os.path.join(settings.DATA_DUMP_DIR,
                                       database.__name__ + '.json'), 'w') as fh:
                    fh.write(obj)
            except Exception as err:
                print("Caught error: %s" % err)
