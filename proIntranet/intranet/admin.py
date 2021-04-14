from django.contrib import admin

# Register your models here.
from .models import Aviso,Publicacion,Documento

admin.site.register(Aviso)
admin.site.register(Publicacion)
admin.site.register(Documento)