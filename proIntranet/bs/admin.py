from django.contrib import admin

#MODELS
from .models import Parametro, Modulo


class ModeloAdminBase(admin.ModelAdmin):
    readonly_fields = ['usu_insercion',
                       'fec_insercion',
                       'usu_modificacion',
                       'fec_modificacion',
                       ]
    list_display = ['__str__',
                    'get_name_usu_insercion',
                    'fec_insercion',
                    'get_name_usu_modificacion',
                    'fec_modificacion',
                    ]


# Register your models here.
admin.site.register(Parametro, ModeloAdminBase)
admin.site.register(Modulo, ModeloAdminBase)
