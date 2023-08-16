from django.urls import path
from django.conf.urls import url
from . import views
from .views import *


app_name = 'intranet'

urlpatterns = [    
    #path('', views.AvisoListView.as_view(), name='index'),
    #path('avisos/', views.ListaAvisos, name='avisos-list'),
    #path('recibo/', views.ListaAvisos, name='recibo'),
   # path('recibo_pdf/', views.GeneratePdf, name='recibo_pdf'),
    path('ver_recibo/', views.ver_recibo, name='ver_recibo'),
    path('ver_recibo2/', views.ver_recibo2, name='ver_recibo2'),
    #path('recibo_pdf2/', views.pdf_generation, name='recibo_pdf2'),
    # path('recibo_pdf2/', views.html_to_pdf_view, name='recibo_pdf2'),
    #path('',views.index,name='index'),
    path('ver_asistencia/', views.ver_asistencia, name='ver_asistencia'),
    # path('ver_asistencia_pdf/', views.ver_asistencia_pdf, name='ver_asistencia_pdf'),

    path('', PublicacionList.as_view(), name='list'),
    path('publicacion/<int:pk>', PublicacionDetail.as_view(), name='detail'),
    path('publicacion/nuevo', PublicacionCreate.as_view(), name='new'),
    path('publicacion/editar/<int:pk>', PublicacionUpdate.as_view(), name='edit'),
    path('publicacion/borrar/<int:pk>', PublicacionDelete.as_view(), name='delete'),
]
    