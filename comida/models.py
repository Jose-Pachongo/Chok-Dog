from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.nombre
    
class menu(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to= 'comida/static/img')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)



