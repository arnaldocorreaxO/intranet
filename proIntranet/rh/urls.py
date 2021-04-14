#Django 
from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
	
	########################
	# DEPENDENCIA
	########################
    path ('dependencia/', views.DependenciaList.as_view(), name='dependencia-list'),
	path ('dependencia/new/', views.DependenciaCreate.as_view(), name='dependencia-new'),
	path ('dependencia/<int:pk>/', views.DependenciaDetail.as_view(), name='dependencia-detail'),    
    path ('dependencia/update/<int:pk>', views.DependenciaUpdate.as_view(), name='dependencia-edit'),
    path ('dependencia/delete/<int:pk>', views.DependenciaDelete.as_view(), name='dependencia-delete'),
    path ('dependencias/', views.getDependencias, name='getDependencias'),
	########################
	# CARGO
	########################
    path ('cargo/', views.CargoList.as_view(), name='cargo-list'),
	path ('cargo/new/', views.CargoCreate.as_view(), name='cargo-new'),
	path ('cargo/<int:pk>/', views.CargoDetail.as_view(), name='cargo-detail'),    
    path ('cargo/update/<int:pk>', views.CargoUpdate.as_view(), name='cargo-edit'),
    path ('cargo/delete/<int:pk>', views.CargoDelete.as_view(), name='cargo-delete'),

	########################
	# INTERNO
	########################
	path ('interno/', views.InternoList.as_view(), name='interno-list'),
	path ('interno/new/', views.InternoCreate.as_view(), name='interno-new'),
	path ('interno/<int:pk>/', views.InternoDetail.as_view(), name='interno-detail'),    
	path ('interno/update/<int:pk>', views.InternoUpdate.as_view(), name='interno-edit'),
	path ('interno/delete/<int:pk>', views.InternoDelete.as_view(), name='interno-delete'),

    ########################
	# AJAX DEPENDENCIAS
	########################
	path('ajax/load-dependencias/', views.load_dependencias, name='ajax_load_dependencias'),

]