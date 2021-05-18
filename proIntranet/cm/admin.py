from cm.models import  Consulta, MotivoConsulta, Paciente
from django.contrib import admin
from bs.admin import ModeloAdminBase


class ConsultaAdmin(ModeloAdminBase):  
    list_display =['fecha','hora','paciente','edad']
    list_filter =['fecha','motivo_consulta','paciente']
    search_fields =['paciente']
    list_display_links = ['fecha','hora','paciente']
    list_per_page = 25
    ordering = ['fecha','hora','paciente']

    def edad(self,obj):
        return obj.paciente.get_edad()
    edad.short_description = 'Edad'
    edad.admin_order_field = 'edad'






# Register your models here.
admin.site.register(Paciente,ModeloAdminBase)
admin.site.register(MotivoConsulta,ModeloAdminBase)
admin.site.register(Consulta,ConsultaAdmin)