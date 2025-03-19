from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    imagen = models.ImageField(upload_to='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
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




from django.db import models

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Sabor(models.Model):
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
    imagen_descripcion = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    fecha_creacion = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_PRODUCTO)
    

    # Relación con ingredientes (solo para personalizables)
    ingredientes = models.ManyToManyField(Ingrediente, related_name="productos", blank=True)

    # Relación con sabores (solo para productos con sabores)
    sabores = models.ManyToManyField(Sabor, blank=True)

    def __str__(self):
        return self.nombre



from django.utils.timezone import now

from django.db import models
from django.contrib.auth.models import User

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
   
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("confirmado", "Confirmado"),
            ("cancelado", "Cancelado")
        ],
        default="pendiente"
    )

    def __str__(self):
        return f"Reserva de {self.usuario} - Mesa {self.mesa}"


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha = models.DateField()
    hora = models.TimeField()
    personas = models.IntegerField()
    mesa = models.ForeignKey('Mesa', on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("confirmado", "Confirmado"),
            ("cancelado", "Cancelado")
        ],
        default="pendiente"
    )


    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    METODOS_PAGO = [
        ('nequi', 'Nequi'),
        ('daviplata', 'Daviplata'),
        ('contra_entrega', 'Contra Entrega'),  # 🔹 Agregado correctamente
    ]
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)
    comprobante = models.ImageField(upload_to="comprobantes/", null=True, blank=True)
    productos = models.JSONField()  # Se almacenará como JSON con los productos y cantidades
    total = models.DecimalField(max_digits=10, decimal_places=0)
    fecha = models.DateTimeField(auto_now_add=True)
    direccion = models.CharField(max_length=255)
    fecha_pedido = models.DateTimeField(default=now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
  # Relación con el usuario
    


    def __str__(self):
        return f"Pedido de {self.nombre} - {self.metodo_pago}"







 
