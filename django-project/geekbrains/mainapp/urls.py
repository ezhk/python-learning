from django.conf.urls import re_path
from django.urls import path

import mainapp.views as mainapp


app_name = 'mainapp'
urlpatterns = [
    path('', mainapp.products, name="index"),
    path('category/<int:pk>', mainapp.products, name="catogory"),
    path('detail/<int:pk>', mainapp.products_details, name="detail"),
]
