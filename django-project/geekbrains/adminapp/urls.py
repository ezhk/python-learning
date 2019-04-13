from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'
urlpatterns = [
    path('users', adminapp.UsersList.as_view(), name='users'),
    path('users/create', adminapp.UserCreate.as_view(), name='user_create'),
    path('users/update/<int:pk>', adminapp.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>', adminapp.UserDelete.as_view(), name='user_delete'),
    path('categories', adminapp.ProductCategoriesList.as_view(), name='categories'),
    path('categories/create', adminapp.ProductCategoryCreate.as_view(), name='category_create'),
    path('categories/update/<int:pk>', adminapp.ProductCategoryUpdate.as_view(), name='category_update'),
    path('categories/delete/<int:pk>', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),
]
