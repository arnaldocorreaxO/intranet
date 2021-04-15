#Django 
from django.db import models
from config.utils import *


#NACIONALIDAD
class Nacionalidad(models.Model):
	denominacion = models.CharField(max_length=100,unique=True)
	estado = models.CharField(max_length=1,choices=choiceEstado(),default='A')
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.denominacion	
#PAIS
class Pais(models.Model):
	cod_pais = models.CharField(max_length=3,unique=True)
	denominacion = models.CharField(max_length=100)
	estado = models.CharField(max_length=1,choices=choiceEstado(),default='A')
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.denominacion	
#DEPARTAMENTOS
class Departamento(models.Model):
	pais = models.ForeignKey(Pais,on_delete=models.CASCADE)
	denominacion = models.CharField(max_length=100)
	estado = models.CharField(max_length=1,choices=choiceEstado(),default='A')
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.denominacion		
#CIUDADES
class Ciudad(models.Model):
	departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE)
	denominacion = models.CharField(max_length=100)
	estado = models.CharField(max_length=1,choices=choiceEstado(),default='A')
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.denominacion