from cm.models import  Consulta, MotivoConsulta, Paciente
from django.contrib import admin
from bs.admin import ModeloAdminBase

# Register your models here.
admin.site.register(Paciente,ModeloAdminBase)
admin.site.register(MotivoConsulta,ModeloAdminBase)
admin.site.register(Consulta,ModeloAdminBase)