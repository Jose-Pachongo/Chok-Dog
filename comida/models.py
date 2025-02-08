from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add = True)

    def _str_(self):
        return self.nombre
    
class menu(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to= 'comida/static/img')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return self.nombre


from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Asegurar que el email sea único

    USERNAME_FIELD = 'email'  # Usar el email en lugar del username
    REQUIRED_FIELDS = ['username']  # Username sigue siendo requerido, pero no para login

    def __str__(self):
        return self.email