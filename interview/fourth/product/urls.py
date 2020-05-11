from django.urls import path

from product.views import ProductView, ProductEditView

app_name = "product"
urlpatterns = [
    path("", ProductView.as_view(), name="index"),
    path("create", ProductEditView.as_view(), name="create"),
]
