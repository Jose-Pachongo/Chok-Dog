
from django import forms
from django.contrib import admin
from .models import productos
from .models import menu
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import MensajeContacto


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



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('phone_number', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'address'),
        }),
    )


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'mensaje')
    search_fields = ('nombre', 'correo')
   