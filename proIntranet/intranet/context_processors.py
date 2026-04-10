# intranet/context_processors.py
from .models import NavbarMenu

from django.db.models import Prefetch
from .models import NavbarMenu, NavbarSection, NavbarItem

from django.db.models import Prefetch
from .models import NavbarMenu, NavbarSection, NavbarItem

def menu_navbar(request):
    # 1. Definimos el prefetch de items ordenados
    prefetch_items = Prefetch(
        'items', 
        queryset=NavbarItem.objects.all().order_by('orden')
    )

    # 2. Definimos el prefetch de secciones ordenadas, que a su vez trae los items
    prefetch_secciones = Prefetch(
        'secciones',
        queryset=NavbarSection.objects.all().order_by('orden').prefetch_related(prefetch_items)
    )

    # 3. Retornamos los menús con toda la jerarquía pre-cargada y ordenada
    return {
        'navbar_menus': NavbarMenu.objects.all().order_by('orden').prefetch_related(prefetch_secciones)
    }