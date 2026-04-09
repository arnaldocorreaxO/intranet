# intranet/context_processors.py
from .models import NavbarMenu

def menu_navbar(request):
    return {
        'navbar_menus': NavbarMenu.objects.all().order_by('orden').prefetch_related('secciones__items')
    }