#DJANGO
from django.contrib.auth.models import User
from django.db import models

#LOCALS
from rh.models import *
from bs.models import *
from bs.utils import *


#PERFIL DE USUARIO
class Perfil(models.Model):
	usuario = models.OneToOneField(User,on_delete =models.CASCADE)
	sede = models.CharField(max_length=3,choices=choiceSede(),default='CEN')
	legajo  = models.IntegerField(null=True,blank=True)
	telefono = models.CharField(max_length=30, blank=True)
	nacionalidad = models.ForeignKey(Nacionalidad,on_delete=models.CASCADE,null=True,blank=True)
	departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE,null=True,blank=True)
	ciudad = models.ForeignKey(Ciudad,on_delete=models.CASCADE,null=True,blank=True)
	direccion = models.CharField(max_length=100, blank=True, null=True)
	genero = models.CharField(max_length=1,choices=choiceGenero(),null=True,blank=True)
	fec_nacimiento = models.DateField(blank=True,null=True)
	fec_vinculacion = models.DateField(blank=True,null=True)#Fecha Nombramiento o Contrato
	tip_empleado = models.CharField(max_length=3,choices=choiceTipoEmpleado(),blank=True,null=True)
	estado_civil = models.CharField(max_length=2,choices=choiceEstadoCivil(),default='DE')
	#dependencia  = models.IntegerField(null=True,blank=True)
	#cargo  = models.IntegerField(null=True,blank=True)
	dependencia = models.ForeignKey(Dependencia,on_delete =models.CASCADE,null=True,blank=True)
	cargo = models.ForeignKey(Cargo,on_delete =models.CASCADE,null=True,blank=True)	
	foto = models.ImageField(
		upload_to = 'usuarios/img/fotos',
		blank=True,
		null=True
		)
	documento_identidad = models.FileField(
		upload_to = 'usuarios/doc/ci',
		blank=True,
		null=True
		)
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)
	
	class meta:
		verbose_name = 'Perfil'
		verbose_name_plural = 'Perfiles'

	def __str__(self):
		return self.usuario.username
