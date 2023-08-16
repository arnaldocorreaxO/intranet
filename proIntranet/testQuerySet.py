""" Programa: Pruebas Queryset xO 
	Creacion: 2019-09-22
	Objetivo: Pruebas Queryset
"""
import os 
from django.contrib.auth.models import User as Usuarios

os.system('clear')

u = Usuarios.objects.all()

for k,v in u.item():
	print(k, ':', v)
