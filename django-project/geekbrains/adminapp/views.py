from django.db.models import F
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.core.paginator import Paginator

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from adminapp.forms import ProductCategoryForm
from authapp.models import ShopUser
from mainapp.models import Products, ProductCategory

from authapp.forms import CreateForm
from orderapp.forms import OrderForm, OrderItemForm
from orderapp.models import Order, OrderItem


class IsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IndexList(IsSuperUserMixin, TemplateView):
    template_name = 'adminapp/index.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(IndexList, self).get_context_data(object_list=None, **kwargs)

        users_page = self.request.GET.get('users_page')
        users_list = ShopUser.objects.all()
        paginator = Paginator(users_list, 3)
        users = paginator.get_page(users_page)

        categories_page = self.request.GET.get('categories_page')
        categories_list = ProductCategory.objects.all()
        paginator = Paginator(categories_list, 3)
        categories = paginator.get_page(categories_page)

        products_page = self.request.GET.get('products_page')
        products_list = Products.objects.all()
        paginator = Paginator(products_list, 3)
        products = paginator.get_page(products_page)

        context.update({
            'users_list': users,
            'categories_list': categories,
            'products_list': products,
        })
        return context


class UsersList(IsSuperUserMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_queryset(self):
        return ShopUser.objects.order_by('-is_active').all()


class UserCreate(IsSuperUserMixin, CreateView):
    model = ShopUser
    form_class = CreateForm
    template_name = 'adminapp/update_user.html'
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        context.update({'title': 'Создание нового пользователя'})
        return context


class UserUpdate(IsSuperUserMixin, UpdateView):
    model = ShopUser
    fields = ('username', 'firstname', 'lastname',
              'email', 'gender', 'age', 'is_active')
    template_name = 'adminapp/update_user.html'

    def get_success_url(self):
        return reverse_lazy('adminapp:user_update',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context.update({'title': f"Изменение пользователя {context.get('object').username}"})
        return context


class UserDelete(IsSuperUserMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/delete_user.html'
    success_url = reverse_lazy('adminapp:users')

    def delete(self, request, *args, **kwargs):
        # first time we only disable category
        user = ShopUser.objects.get(pk=self.kwargs.get('pk'))
        if user.is_active:
            user.is_active = False
            user.save()
            return HttpResponseRedirect(reverse_lazy('adminapp:users'))

        # second time we remove category
        return super(UserDelete, self).delete(request, *args, **kwargs)


class ProductCategoriesList(IsSuperUserMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_queryset(self):
        return ProductCategory.objects.order_by('-is_active').all()


class ProductCategoryCreate(IsSuperUserMixin, CreateView):
    model = ProductCategory
    fields = '__all__'
    template_name = 'adminapp/update_category.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreate, self).get_context_data(**kwargs)
        context.update({'title': 'Создание новой категории'})
        return context


class ProductCategoryUpdate(IsSuperUserMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/update_category.html'
    form_class = ProductCategoryForm

    def get_success_url(self):
        return reverse_lazy('adminapp:category_update',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdate, self).get_context_data(**kwargs)
        context.update({'title': f"Изменение категории {context.get('object').name}"})
        return context

    def form_valid(self, form):
        discount = form.cleaned_data.get('discount', 0)
        if discount > 0:
            self.object.products_set.update(
                price=F('price') * (1 - discount / 100)
            )
        return super(ProductCategoryUpdate, self).form_valid(form)


class ProductCategoryDelete(IsSuperUserMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/delete_category.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        # first time we only disable category
        category = ProductCategory.objects.get(pk=self.kwargs.get('pk'))
        if category.is_active:
            category.is_active = False
            category.save()
            return HttpResponseRedirect(reverse_lazy('adminapp:categories'))

        # second time we remove category
        return super(ProductCategoryDelete, self).delete(request, *args, **kwargs)


class ProductsList(IsSuperUserMixin, ListView):
    model = Products
    template_name = 'adminapp/products.html'

    def get_queryset(self):
        return Products.objects.select_related('category').order_by('-is_active').all()


class ProductCreate(IsSuperUserMixin, CreateView):
    model = Products
    fields = '__all__'
    template_name = 'adminapp/update_product.html'
    success_url = reverse_lazy('adminapp:products')

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context.update({'title': 'Создание нового продукта'})
        return context


class ProductUpdate(IsSuperUserMixin, UpdateView):
    model = Products
    fields = '__all__'
    template_name = 'adminapp/update_product.html'

    def get_success_url(self):
        return reverse_lazy('adminapp:product_update',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context.update({'title': f"Изменение продукта {context.get('object').name}"})
        return context


class ProductDelete(IsSuperUserMixin, DeleteView):
    model = Products
    template_name = 'adminapp/delete_product.html'
    success_url = reverse_lazy('adminapp:products')

    def delete(self, request, *args, **kwargs):
        # first time we only disable category
        category = Products.objects.get(pk=self.kwargs.get('pk'))
        if category.is_active:
            category.is_active = False
            category.save()
            return HttpResponseRedirect(reverse_lazy('adminapp:products'))

        # second time we remove category
        return super(ProductDelete, self).delete(request, *args, **kwargs)


class OrderStatus(IsSuperUserMixin, UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'adminapp/order_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderForm, extra=0)

        context['formset'] = order_formset(self.request.POST or None, instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('admin:order_update', kwargs={'pk': self.kwargs.get('pk'), })

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            formset.instance = form.save()
            formset.save()

        return super().form_valid(form)
