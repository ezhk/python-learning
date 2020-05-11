from django.urls import path

from product.views import ProductView, create

app_name = "product"
urlpatterns = [
    path("", ProductView.as_view(), name="index"),
    path("create", create, name="create")
]
