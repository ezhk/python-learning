from django.urls import path

from orderapp.views import OrderList, OrderCreate, OrderRead, OrderUpdate, OrderDelete, change_order_status

app_name = 'orderapp'
urlpatterns = [
    path('', OrderList.as_view(), name='index'),
    path('create', OrderCreate.as_view(), name='create'),
    path('read/<int:pk>', OrderRead.as_view(), name='read'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>', OrderDelete.as_view(), name='delete'),

    path('update/<int:pk>/status/<slug:status>', change_order_status, name='update_status'),
]
