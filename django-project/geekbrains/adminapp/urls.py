from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'
urlpatterns = [
    path('', adminapp.IndexList.as_view(), name='index'),

    path('users', adminapp.UsersList.as_view(), name='users'),
    path('users/create', adminapp.UserCreate.as_view(), name='user_create'),
    path('users/update/<int:pk>', adminapp.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>', adminapp.UserDelete.as_view(), name='user_delete'),

    path('categories', adminapp.ProductCategoriesList.as_view(), name='categories'),
    path('categories/create', adminapp.ProductCategoryCreate.as_view(), name='category_create'),
    path('categories/update/<int:pk>', adminapp.ProductCategoryUpdate.as_view(), name='category_update'),
    path('categories/delete/<int:pk>', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),

    path('products', adminapp.ProductsList.as_view(), name='products'),
    path('products/create', adminapp.ProductCreate.as_view(), name='product_create'),
    path('products/update/<int:pk>', adminapp.ProductUpdate.as_view(), name='product_update'),
    path('products/delete/<int:pk>', adminapp.ProductDelete.as_view(), name='product_delete'),

    path('order/update/<int:pk>', adminapp.OrderStatus.as_view(), name='order_update'),
]
