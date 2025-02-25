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
    path('perfil', views.perfil, name='perfil'),
    path('logout', views.logout_request, name='logout'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservar/', views.procesar_reserva, name='procesar_reserva'),
     path('obtener_mesas_disponibles/', views.obtener_mesas_disponibles, name='obtener_mesas_disponibles'),
    path('reservar/', views.procesar_reserva, name='procesar_reserva'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

