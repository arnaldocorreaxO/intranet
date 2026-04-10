# intranet/context_processors.py
from .models import NavbarMenu

from django.db.models import Prefetch
from .models import NavbarMenu, NavbarSection, NavbarItem

def menu_navbar(request):
    # Definimos el orden para las secciones
    prefetch_secciones = Prefetch(
        'secciones',
        queryset=NavbarSection.objects.all().order_by('orden'),
        to_attr='secciones_ordenadas'
    )
    
    # Definimos el orden para los items dentro de cada sección
    # Nota: Esto requiere que el prefetch sea anidado o que el modelo 
    # NavbarSeccion tenga definido el ordenamiento por defecto.
    
    return {
        'navbar_menus': NavbarMenu.objects.all().order_by('orden').prefetch_related(
            Prefetch(
                'secciones',
                queryset=NavbarSection.objects.all().order_by('orden').prefetch_related(
                    Prefetch('items', queryset=NavbarItem.objects.all().order_by('orden'))
                )
            )
        )
    }