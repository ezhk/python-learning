from django.contrib import admin
from mainapp.models import Products, \
                           Properties, \
                           ProductCategory, \
                           ProductAndProperty

from authapp.models import ShopUser

admin.site.register(Products)
admin.site.register(Properties)
admin.site.register(ProductCategory)
admin.site.register(ProductAndProperty)

admin.site.register(ShopUser)