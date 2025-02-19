from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Productos, Menu, MensajeContacto

User = get_user_model()

class UserAdmin(UserAdmin):
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

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'fecha_creacion')
    list_display_links = ('nombre',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen', 'precio')
    list_display_links = ('nombre',)

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'mensaje')
    search_fields = ('nombre', 'correo')


