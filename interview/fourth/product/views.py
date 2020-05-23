from django.views import View
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm()

        return context


class ProductEditView(View):
    """
    Class for operations with product, such as create or get product form.
    Using templates for this operations, that defined below.

    Why did two methods?
    POST might be correct or not, and when form is invalid —
        we have to show invalid fields.
        On next open form, fields will be marked incorrect as previous open operation.
    So when need to get empty form — we use GET — receive form without suggestions.
    When need save or show invalid form — use POST method.
    """

    FORM_TEMPLATE = "product/product_form.html"
    TABLE_TEMPLATE = "product/product_table.html"

    def get(self, request, *args, **kwargs):
        """
        Return empty rendered form, without error suggest.
        """

        return render(
            request,
            self.__class__.FORM_TEMPLATE,
            {"form": ProductForm()},
            status=200,
        )

    def post(self, request, *args, **kwargs):
        """
        Create product if form is valid
            or return status code 400
            and form with suggest errors.
        """

        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                self.__class__.TABLE_TEMPLATE,
                {
                    "object_list": Product.objects.select_related("provider")
                    .all()
                    .order_by("created_at")
                },
            )

        return render(
            request, self.__class__.FORM_TEMPLATE, {"form": form}, status=400,
        )
