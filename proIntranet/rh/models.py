from django.db import models
from django.forms.models import model_to_dict
from bs.utils import *


#DEPENDENCIAS
class Dependencia(models.Model):
	dependencia_padre = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
	denominacion = models.CharField(max_length=100,unique=True)
	sede = models.CharField(max_length=3,choices=choiceSede(),default='CEN')
	estado = models.CharField(max_length=1,choices=choiceEstado(),default='A')
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)	
	class meta:
		verbose_name = 'Dependencia'
		verbose_name_plural = 'Dependencias'
		ordering = ['denominacion']

	def __str__(self):
		return self.denominacion	
#CARGOS
class Cargo(models.Model):
	denominacion = models.CharField(max_length=100,unique=True)
	estado = models.CharField(max_length=1,choices=choiceEstado(),default='A')
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)
	class meta:
		verbose_name = 'Cargo'
		verbose_name_plural = 'Cargos'

	def __str__(self):
		return self.denominacion
#NUMERO DE INTERNOS		
class Interno(models.Model):	
	dependencia = models.CharField(max_length=250)
	responsable = models.CharField(max_length=250,null=True,blank=True)
	extension = models.IntegerField()
	sede = models.CharField(max_length=3,choices=choiceSede(),default='CEN')

	def __str__(self):
		return str(self.extension)
