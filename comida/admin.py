from pyexpat import model
from django.contrib import admin
from .models import productos
from .models import menu

# Register your models here.

class productosAdmin(admin.ModelAdmin):
    model = productos
    list_display = ('nombre','descripcion','precio','fecha_creacion')
    list_display_links = ('nombre',)
admin.site.register(productos, productosAdmin)

class menuAdmin(admin.ModelAdmin):
    model = menu
    list_display = ('nombre','imagen','precio',)
    list_display_links = ('nombre',)
admin.site.register(menu, menuAdmin)