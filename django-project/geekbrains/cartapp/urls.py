from django.urls import path
import cartapp.views as cartapp


app_name = 'cartapp'
urlpatterns = [
    path('', cartapp.show, name='index'),
    path('add/<int:pk>', cartapp.add, name='add'),
    path('delete/<int:pk>', cartapp.delete, name='delete'),
    path('update/<int:pk>/quantity/<int:value>', cartapp.update, name='update'),
]