from django.urls import path
from .views import *


app_name = 'intranet'

urlpatterns = [    
    path('', PublicacionList.as_view(), name='list'),
    path('publicacion/<int:pk>', PublicacionDetail.as_view(), name='detail'),
    path('publicacion/nuevo', PublicacionCreate.as_view(), name='new'),
    path('publicacion/editar/<int:pk>', PublicacionUpdate.as_view(), name='edit'),
    path('publicacion/borrar/<int:pk>', PublicacionDelete.as_view(), name='delete'),

    path('ver_recibo/', ver_recibo, name='ver_recibo'),
    path('ver_recibo2/', ver_recibo2, name='ver_recibo2'),
    path('ver_asistencia/', ver_asistencia, name='ver_asistencia'),
]
    