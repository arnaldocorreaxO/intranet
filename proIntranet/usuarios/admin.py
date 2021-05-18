from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Perfil)

class PerfilAdmin(admin.ModelAdmin):
	list_display=('usuario','legajo','usuario_full_name','sede','creacion')
	search_fields = ['usuario__username','legajo','usuario__first_name','usuario__last_name']
	list_filter = ('sede','tip_empleado','usuario__is_active','creacion')

	def usuario_full_name(self,obj):
		return f"{obj.usuario.first_name} {obj.usuario.last_name}"
		
