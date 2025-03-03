from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Menu, MensajeContacto
from .models import Reserva
from .models import Profile
from .models import Mesa

admin.site.register(Mesa)

admin.site.register(Reserva)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

admin.site.register(Profile, ProfileAdmin)

User = get_user_model()
# class ProductAdmin(admin.ModelAdmin):
#     model = Product
#     list_display = ('imagen', 'nombre', 'descripcion', 'precio')
# admin.site.register(Product, ProductAdmin)

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





# from django.contrib import admin
# from .models import Producto, Ingrediente, Sabor

# class ProductoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'tipo', 'precio')
#     list_filter = ('tipo',)
#     search_fields = ('nombre',)

# admin.site.register(Producto, ProductoAdmin)
# admin.site.register(Ingrediente)
# admin.site.register(Sabor)

from django.contrib import admin
from django import forms
from .models import Producto, Ingrediente, Sabor

# Creamos un formulario para personalizar el admin
class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        widgets = {
            'ingredientes': forms.CheckboxSelectMultiple()  # Permite seleccionar varios ingredientes
        }

# Registramos el modelo con el formulario personalizado
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoAdminForm
    list_display = ("nombre", "tipo", "precio")
    search_fields = ('nombre',)
    

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ingrediente)
admin.site.register(Sabor)

