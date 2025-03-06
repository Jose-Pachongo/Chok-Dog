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


from django.utils.safestring import mark_safe
import json
from django.contrib import admin
from comida.models import Pedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'metodo_pago', 'get_productos', 'total', 'direccion', 'fecha_pedido')

    def get_productos(self, obj):
        try:
            productos = json.loads(obj.productos) if isinstance(obj.productos, str) else obj.productos
            productos_html = "<ul>"
            for producto in productos:
                productos_html += f"<li><strong>{producto['nombre']}</strong> - Cantidad: {producto['cantidad']} - Precio: {producto['precio']}<br>"
                if producto['ingredientes']:
                    productos_html += f"<em>Ingredientes:</em> {', '.join(producto['ingredientes'])}<br>"
                productos_html += "</li><hr>"
            productos_html += "</ul>"
            return mark_safe(productos_html)
        except Exception as e:
            return f"Error al mostrar productos: {e}"

    get_productos.short_description = "Productos"

admin.site.register(Pedido, PedidoAdmin)



