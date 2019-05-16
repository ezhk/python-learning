from django.urls import path
import authapp.views as authapp

from authapp.views import CreateShopUser

app_name = 'authapp'
urlpatterns = [
    path('', authapp.login, name='login'),
    path('logout', authapp.logout, name='logout'),
    path('create', CreateShopUser.as_view(), name='create'),
    path('edit', authapp.edit, name='edit'),
    path('verify/<str:email>/<slug:activation_key>', authapp.verify, name='verify'),
]
