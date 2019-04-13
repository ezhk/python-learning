"""geekbrains URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path

from django.conf import settings
from django.conf.urls import handler404, \
    handler500
from django.conf.urls.static import static

import mainapp.views as view

handler404 = view.page404
handler500 = view.page500

urlpatterns = [
    re_path(r'^$', view.main, name='index'),
    re_path(r'^contacts/$', view.contacts, name='contacts'),
    re_path(r'^products/', include('mainapp.urls', namespace='products')),
    re_path(r'^auth/', include('authapp.urls', namespace='auth')),
    re_path(r'^cart/', include('cartapp.urls', namespace='cart')),
    re_path(r'^admin/', include('adminapp.urls', namespace='admin'))
    # re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
