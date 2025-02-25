from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Product, Menu, MensajeContacto
from .models import Reserva
from .models import Profile
from .models import Mesa

admin.site.register(Mesa)

admin.site.register(Reserva)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

admin.site.register(Profile, ProfileAdmin)

User = get_user_model()
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('imagen', 'nombre', 'descripcion', 'precio')
admin.site.register(Product, ProductAdmin)

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



@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'mensaje')
    search_fields = ('nombre', 'correo')



