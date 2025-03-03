from django.db import models


from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    imagen = models.ImageField(upload_to='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Menu(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='comida/static/img')
    precio = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.nombre


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    mensaje = models.TextField()

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.correo})"

from django.db import models

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()

    def __str__(self):
        return f"Mesa {self.numero} - Capacidad: {self.capacidad}"


class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha = models.DateField()
    hora = models.TimeField()
    personas = models.IntegerField()
    mesa = models.ForeignKey('Mesa', on_delete=models.CASCADE, null=True, blank=True)

  # Referencia a Mesa

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"


from django.db import models

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPOS_PRODUCTO = [
        ('personalizable', 'Personalizable'),
        ('sabores', 'Con Sabores'),
        ('simple', 'Simple'),
        ('bebida', 'Bebida'),
    ]

    imagen = models.ImageField(upload_to='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_PRODUCTO)

    # Relación con ingredientes (solo para personalizables)
    ingredientes = models.ManyToManyField(Ingrediente, related_name="productos", blank=True)

    # Relación con sabores (solo para productos con sabores)
    sabores = models.ManyToManyField("Sabor", related_name="productos", blank=True)

    def __str__(self):
        return self.nombre

class Sabor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre





 
