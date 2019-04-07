from django.contrib import admin
from mainapp.models import Products, \
    Properties, \
    ProductCategory, \
    ProductAndProperty, \
    FeedBack

admin.site.register(Products)
admin.site.register(Properties)
admin.site.register(ProductCategory)
admin.site.register(ProductAndProperty)
admin.site.register(FeedBack)
