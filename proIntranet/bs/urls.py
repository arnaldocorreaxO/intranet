#Django 
from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
	
	########################
	# CIUDADES
	########################
	path('ajax/get-ciudades/', views.getCiudades, name='getCiudades'),
	path('ajax/get-persona/', views.getPersona, name='getPersona'),
	path('ajax/load-ciudades/', views.load_ciudades, name='ajax_load_ciudades'),
	

]