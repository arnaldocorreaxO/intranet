from datetime import datetime
from django.db.models.deletion import CASCADE, PROTECT
from config.utils import choiceEstadoCivil, choiceGenero
from enum import unique
from django.db import models
from bs.models import ModeloBase, Nacionalidad

'''PACIENTES'''
class Paciente(ModeloBase):
    ci = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    sexo = models.CharField(choices=choiceGenero(),max_length=2)
    estado_civil = models.CharField(choices=choiceEstadoCivil(),max_length=2)
    nacionalidad = models.ForeignKey(Nacionalidad,on_delete=PROTECT)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


'''HISTORIA CLINICA'''
class MotivoConsulta(ModeloBase):   
    descripcion = models.CharField(max_length=150,unique=True)
    


'''HISTORIA CLINICA'''
class Consulta(ModeloBase):   
    fecha = models.DateField(default=datetime.today)
    hora = models.TimeField(null=True,blank=True)
    paciente = models.ForeignKey(Paciente,on_delete=PROTECT)
    motivo_consulta = models.ManyToManyField(MotivoConsulta)
    descripcion = models.TextField()
    indicacion_medica = models.TextField()

    def __str__(self):
        return f"{self.fecha} {self.hora} {self.paciente}"
    
    
