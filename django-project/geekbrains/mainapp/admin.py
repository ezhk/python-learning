from django.contrib import admin
from mainapp.models import Products, \
                           Properties, \
                           ProductCategory, \
                           ProductAndProperty

admin.site.register(Products)
admin.site.register(Properties)
admin.site.register(ProductCategory)
admin.site.register(ProductAndProperty)