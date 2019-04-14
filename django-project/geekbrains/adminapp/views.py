from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from authapp.models import ShopUser
from mainapp.models import ProductCategory

from authapp.forms import CreateForm


class IsSuperUserView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class UsersList(IsSuperUserView, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_queryset(self):
        return ShopUser.objects.order_by('-is_active').all()


class UserCreate(IsSuperUserView, CreateView):
    model = ShopUser
    form_class = CreateForm
    template_name = 'adminapp/update_user.html'
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        context.update({'title': 'Создание нового пользователя'})
        return context


class UserUpdate(IsSuperUserView, UpdateView):
    model = ShopUser
    fields = ('username', 'firstname', 'lastname',
              'email', 'gender', 'age', 'avatar',
              'is_active')
    template_name = 'adminapp/update_user.html'

    def get_success_url(self):
        return reverse_lazy('adminapp:user_update',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context.update({'title': f"Изменение пользователя {context.get('object').username}"})
        return context


class UserDelete(IsSuperUserView, DeleteView):
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


class ProductCategoriesList(IsSuperUserView, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_queryset(self):
        return ProductCategory.objects.order_by('-is_active').all()


class ProductCategoryCreate(IsSuperUserView, CreateView):
    model = ProductCategory
    fields = '__all__'
    template_name = 'adminapp/update_category.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreate, self).get_context_data(**kwargs)
        context.update({'title': 'Создание новой категории'})
        return context


class ProductCategoryUpdate(IsSuperUserView, UpdateView):
    model = ProductCategory
    fields = '__all__'
    template_name = 'adminapp/update_category.html'

    def get_success_url(self):
        return reverse_lazy('adminapp:category_update',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdate, self).get_context_data(**kwargs)
        context.update({'title': f"Изменение категории {context.get('object').name}"})
        return context


class ProductCategoryDelete(IsSuperUserView, DeleteView):
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
