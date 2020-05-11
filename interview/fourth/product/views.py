from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render

from product.forms import ProductForm
from product.models import Product, Provider


class ProductView(ListView):
    model = Product

    def get_queryset(self):
        return (
            Product.objects.select_related("provider")
            .all()
            .order_by("created_at")
        )


def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProductForm()

    return render(request, "product/product_create.html", {"form": form})
