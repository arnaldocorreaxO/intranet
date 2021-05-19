from datetime import datetime
from enum import unique

from bs.models import ModeloBase, Nacionalidad
from config.utils import calculate_age, choiceEstadoCivil, choiceGenero
from django.db import models
from django.db.models.deletion import PROTECT
from django.forms import model_to_dict

'''PACIENTES'''
class Paciente(ModeloBase):
    ci = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(choices=choiceGenero(),max_length=2)
    estado_civil = models.CharField(choices=choiceEstadoCivil(),max_length=2)
    nacionalidad = models.ForeignKey(Nacionalidad,on_delete=PROTECT)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_edad(self):
        return calculate_age(self.fecha_nacimiento)
    
    def toJSON(self):
        item = model_to_dict(self,exclude=[''])
        item['fecha_nacimiento'] = self.fecha_nacimiento.strftime('%d-%m-%Y')
        item['edad'] = self.get_edad()
        return item

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Paciente, self).save(force_insert, force_update)


'''MOTIVOS DE CONSULTAS'''
class MotivoConsulta(ModeloBase):   
    descripcion = models.CharField(max_length=150,unique=True)
    
    def __str__(self):
        return f"{self.descripcion}"

'''HISTORIA CLINICA'''
class Consulta(ModeloBase):   
    fecha = models.DateField(default=datetime.today)
    hora = models.TimeField(null=True,blank=True)
    paciente = models.ForeignKey(Paciente,on_delete=PROTECT)
    motivo_consulta = models.ForeignKey(MotivoConsulta,on_delete=PROTECT)
    descripcion = models.TextField()
    indicacion_medica = models.TextField()

    def __str__(self):
        return f"{self.fecha} {self.hora} {self.paciente}"
    
    def toJSON(self):
        item = model_to_dict(self,exclude=[''])
        item['fecha'] = self.fecha.strftime('%d/%m/%Y')
        item['hora'] = self.hora.strftime('%H:%M:%S')
        item['paciente'] = str(self.paciente)
        item['edad'] = self.paciente.get_edad()
        return item
    
    
