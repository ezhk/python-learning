from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'
urlpatterns = [
    path('', mainapp.products, name="index"),
    path('category/<int:pk>/ajax', cache_page(1800)(mainapp.products), name="category-ajax"),
    path('category/<int:pk>', mainapp.products, name="category"),
    path('detail/<int:pk>', mainapp.products_details, name="detail"),
]
