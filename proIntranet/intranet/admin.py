from django.contrib import admin

# Register your models here.
from .models import Aviso,Publicacion,Documento

admin.site.register(Aviso)
admin.site.register(Publicacion)
admin.site.register(Documento)

# admin.py
from django.contrib import admin
from .models import NavbarMenu, NavbarSection, NavbarItem

class NavbarItemInline(admin.TabularInline):
    model = NavbarItem
    extra = 1

class NavbarSectionInline(admin.TabularInline):
    model = NavbarSection
    extra = 1

@admin.register(NavbarMenu)
class NavbarMenuAdmin(admin.ModelAdmin):
    inlines = [NavbarSectionInline]
    list_display = ("nombre", "orden")

@admin.register(NavbarSection)
class NavbarSectionAdmin(admin.ModelAdmin):
    inlines = [NavbarItemInline]
    list_display = ("titulo", "menu", "orden")

@admin.register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "section", "orden")
