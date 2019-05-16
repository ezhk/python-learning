from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.forms import inlineformset_factory

from orderapp.forms import OrderForm, OrderItemForm
from orderapp.models import Order, OrderItem

from cartapp.models import ShopCart


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderRead(DetailView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = ()
    success_url = reverse_lazy('orderapp:index')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderForm, extra=1)

        formset = OrderFormSet(self.request.POST or None)
        if not self.request.POST and self.request.user.cart:
            cart = ShopCart.objects.filter(user=self.request.user)
            OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                 form=OrderForm,
                                                 extra=len(cart))
            formset = OrderFormSet()
            for id, form in enumerate(formset.forms):
                form.initial.update({
                    'product': cart[id].product,
                    'quantity': cart[id].quantity,
                    'price': cart[id].product.price,
                })

        context['confirm_button'] = 'Оформить заказ'
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            form.instance.user = self.request.user
            if formset.is_valid():
                formset.instance = form.save()
                formset.save()
            ShopCart.objects.filter(user=self.request.user).delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = ()

    def get_success_url(self):
        return reverse_lazy('orderapp:update',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)

        context['confirm_button'] = 'Сохранить изменения'
        formset = OrderFormSet(data=self.request.POST or None, instance=self.object)
        for form in formset.forms:
            if form.instance.pk:
                form.initial.update({'price': form.instance.product.price})
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            formset.instance = form.save()
            formset.save()
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orderapp:index')


def change_order_status(request, pk, status):
    if request.user.is_superuser or (
            status == Order.ORDER_STATUS_PROCESSING
            and Order.objects.filter(user=request.user, pk=pk)
    ):
        order = get_object_or_404(Order, pk=pk)
        order.status = status
        order.save()

        return HttpResponseRedirect(reverse_lazy('orderapp:index'))
    return HttpResponseForbidden("You cannot change order status")
