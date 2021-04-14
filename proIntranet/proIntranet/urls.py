"""proIntranet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
	path('', include('intranet.urls',namespace='publicacion')),
    path('usuarios/', include('usuarios.urls')),
    path('rh/', include('rh.urls')),
    path('bs/', include('bs.urls')),
    # path('publicacion/',include('intranet.urls',namespace='publicacion')),
    path('admin/', admin.site.urls),
    #  path(
    #     'change-password/',
    #     auth_views.PasswordChangeView.as_view(template_name='usuarios/change-password.html'),
    #     name ='change-password',
    # ),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('intranet/', AvisoListView.as_view(), name='aviso-list'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#TITULO ADMINISTRACION DJANGO
admin.site.site_header = 'Administración Intranet INC'