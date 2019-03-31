from django.contrib import admin
from mainapp.models import ProductCategory, Products, ProductProperty

admin.site.register(ProductCategory)
admin.site.register(Products)
admin.site.register(ProductProperty)