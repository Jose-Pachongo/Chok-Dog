from django.db import models
from django.contrib.auth.models import AbstractUser

class productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class menu(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='comida/static/img')
    precio = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    mensaje = models.TextField()

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.correo})"

