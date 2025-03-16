from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Menu, MensajeContacto
from .models import Reserva
from .models import Profile
from .models import Mesa

admin.site.register(Mesa)



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

admin.site.register(Profile, ProfileAdmin)

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


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'mensaje')
    search_fields = ('nombre', 'correo')



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

@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

# Registramos el modelo con el formulario personalizado
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoAdminForm
    list_display = ("nombre", "tipo", "precio", 'imagen', 'imagen_descripcion')
    search_fields = ('nombre',)
    filter_horizontal = ("sabores",) 
    

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ingrediente)




from .models import Pedido


import json
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Pedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'metodo_pago', 'total', 'fecha_pedido', 'estado')
    list_editable = ('estado',)  # Permite editar el estado desde el panel de admin
    actions = ['marcar_como_cancelado']  # Agregamos la acción para cancelar pedidos
    readonly_fields = ('productos_formateados',)  # Mostramos los productos formateados

    def productos_formateados(self, obj):
        """Devuelve los productos en formato HTML legible."""
        if not obj.productos:
            return "No hay productos"
        
        try:
            productos = json.loads(json.dumps(obj.productos))  # Asegurar formato JSON
            html = "<ul>"
            for producto in productos:
                html += f"<li><strong>{producto['nombre']}</strong> - {producto['cantidad']}x ${producto['precio']:,} <br>"
                html += f"Ingredientes: {', '.join(producto['ingredientes']) if producto['ingredientes'] else 'Ninguno'}</li>"
            html += "</ul>"
            return mark_safe(html)  # Permite mostrar HTML en el admin
        except Exception as e:
            return f"Error al formatear productos: {e}"

    productos_formateados.short_description = "Productos (Formateado)"


admin.site.register(Pedido, PedidoAdmin)

from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'estado')  # Agregamos 'estado'
    list_filter = ('estado',)  # Permite filtrar por estado en el panel
    search_fields = ('nombre', 'fecha', 'hora')  # Agrega búsqueda por estos campos

admin.site.register(Reserva, ReservaAdmin)




