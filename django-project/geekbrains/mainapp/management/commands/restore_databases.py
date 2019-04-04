import os

from mainapp.models import ProductCategory, \
                           Products,        \
                           Properties,      \
                           ProductAndProperty
from django.core.management.base import BaseCommand
from django.core import serializers
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        for database in ProductCategory, Products, Properties, ProductAndProperty:
            try:
                with open(os.path.join(settings.DATA_DUMP_DIR,
                                       database.__name__ + '.json'), 'r') as fh:
                    database.objects.all().delete()
                    for deserialized_object in serializers.deserialize("json", fh.read()):
                        deserialized_object.save()
            except Exception as err:
                print("Caught error: %s" % err)
