"""
URL configuration for sitio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from comida import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from comida.views import lista_productos
from comida.views import pagina_pago, procesar_pedido
from comida.views import profile_view 
from comida.views import eliminar_foto
from comida.views import  eliminar_reserva
from comida.views import cancelar_pedido
from comida.views import historial
from comida.views import cancelar_reserva


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('nosotros',views.nosotros,name='nosotros'),
    path('servicios',views.servicios,name='servicios'),
    path('contactenos',views.contactenos,name='contactenos'),
    path('iniciar',views.iniciar,name='iniciar'),
    path('regis',views.regis,name='regis'),
    path('pagina', views.pagina, name='pagina'),
    path('productos', views.productos, name='productos'),
    path('carrito', views.carrito, name='carrito'),
    path("perfil/", profile_view, name="perfil"),
    path("eliminar-foto/", eliminar_foto, name="eliminar_foto"),
    path('logout', views.logout_request, name='logout'),
    path('reservas/', views.reservas, name='reservas'),
    path('obtener_mesas_disponibles/', views.obtener_mesas_disponibles, name='obtener_mesas_disponibles'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path('cambiar_contrasena/<uidb64>/<token>/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('pago', views.pagina_pago, name='pagina_pago'),
    path("productos/", lista_productos, name="productos"),
    path('procesar_pedido/', procesar_pedido, name='procesar_pedido'),
    path('manual', views.manual, name='manual'),
    path('historial', views.historial, name='historial'),
    
    # path('confirmacion_contrasena/', views.confirmacion_contrasena, name='confirmacion_contrasena'),
    
    path('eliminar_reserva/<int:reserva_id>/', eliminar_reserva, name='eliminar_reserva'),  
    path('cancelar_pedido/<int:pedido_id>/', cancelar_pedido, name='cancelar_pedido'), 
   
    path("cancelar_reserva/<int:reserva_id>/", cancelar_reserva, name="cancelar_reserva"), 
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

