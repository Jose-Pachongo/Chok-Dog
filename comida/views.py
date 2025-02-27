from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MensajeContacto
from .models import Product
from .forms import MensajeContactoForm, CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile  
from datetime import datetime
from .models import Reserva, Mesa
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated:
        return redirect('pagina')
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def servicios(request):
    return render(request, 'servicios.html')

def contactenos(request):
    if request.method == "POST":
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            telefono = form.cleaned_data['telefono']
            mensaje = form.cleaned_data['mensaje']

            subject = "Nuevo mensaje de contacto"
            message = f"""
            Nombre: {nombre}
            Correo: {correo}
            Teléfono: {telefono}

            Mensaje:
            {mensaje}
            """
            
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, ['pjoseedier@gmail.com'])
                messages.success(request, "Mensaje enviado con éxito.")
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")
                print(f"Error de correo: {e}")

            return redirect('contactenos')
    else:
        form = MensajeContactoForm()

    return render(request, "contactenos.html", {"form": form})

@csrf_protect
def regis(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone', '')  # Agregado
        address = request.POST.get('address', '')  # Agregado
        password = request.POST.get('password', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'regis.html', {'error': 'El nombre de usuario ya está en uso.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'regis.html', {'error': 'El correo electrónico ya está en uso.'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Crear un perfil vinculado al usuario
        Profile.objects.create(user=user, phone_number=phone_number, address=address)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"{user.first_name} Bienvenido a Chock Dog.")
            return render(request, 'pagina.html')

    return render(request, 'regis.html')

@csrf_protect
def iniciar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"{user.username} Bienvenido a Chock Dog, has iniciado sesión correctamente.")
            return redirect('pagina')
        else:
            return render(request, 'iniciar.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'iniciar.html')

def pagina(request):
    return render(request, 'pagina.html')

def productos(request):
    products = Product.objects.all()
    return render(request, 'productos.html', {'products': products})
    

def carrito(request):
    return render(request, 'carrito.html')

def perfil(request):
    return render(request, 'perfil.html')

def logout_request(request):
    logout(request)
    return redirect("home")

@login_required
def perfil_view(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']

            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
        except Exception as e:
            messages.error(request, 'Error al actualizar el perfil.')

    return render(request, 'perfil.html')



#reservas


def reservas(request):
    mesas = Mesa.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        personas = request.POST.get('personas')
        mesa_id = request.POST.get('mesa')

        try:
            fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de fecha incorrecto.")
            return redirect('reservas')

        if fecha_reserva < datetime.now().date():
            messages.error(request, "No puedes seleccionar una fecha pasada.")
            return redirect('reservas')

        try:
            hora_reserva = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            messages.error(request, "Formato de hora incorrecto.")
            return redirect('reservas')

        if not (datetime.strptime('17:00', '%H:%M').time() <= hora_reserva <= datetime.strptime('23:00', '%H:%M').time()):
            messages.error(request, "La hora debe estar entre las 17:00 y las 23:00.")
            return redirect('reservas')

        if Reserva.objects.filter(fecha=fecha, hora=hora, mesa_id=mesa_id).exists():
            messages.error(request, "La mesa seleccionada ya está reservada para esa fecha y hora.")
            return redirect('reservas')

        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            messages.error(request, "La mesa seleccionada no existe.")
            return redirect('reservas')

        reserva = Reserva.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            fecha=fecha_reserva,
            hora=hora_reserva,
            personas=personas,
            mesa=mesa
        )
        print("Reserva creada:", reserva)

      
        subject = "Nueva reserva de mesa"
        message = (
            f"Se ha realizado una nueva reserva:\n\n"
            f"Nombre: {nombre}\n"
            f"Correo: {email}\n"
            f"Teléfono: {telefono}\n"
            f"Fecha: {fecha}\n"
            f"Hora: {hora}\n"
            f"Mesa: {mesa.numero}\n"
            f"Número de personas: {personas}\n"
        )

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['pjoseedier@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Reserva realizada y correo enviado con éxito.")
        except Exception as e:
            messages.error(request, f"Reserva realizada, pero hubo un error al enviar el correo: {e}")

        return redirect('reservas')

    return render(request, 'reservas.html', {'mesas': mesas})


def procesar_reserva(request):
    mesas = Mesa.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        personas = request.POST.get('personas')
        mesa_id = request.POST.get('mesa')

        try:
            fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de fecha incorrecto.")
            return redirect('procesar_reserva')

        if fecha_reserva < datetime.now().date():
            messages.error(request, "No puedes seleccionar una fecha pasada.")
            return redirect('procesar_reserva')

        try:
            hora_reserva = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            messages.error(request, "Formato de hora incorrecto.")
            return redirect('procesar_reserva')

        if not (datetime.strptime('17:00', '%H:%M').time() <= hora_reserva <= datetime.strptime('23:00', '%H:%M').time()):
            messages.error(request, "La hora debe estar entre las 17:00 y las 23:00.")
            return redirect('procesar_reserva')

        if Reserva.objects.filter(fecha=fecha, hora=hora, mesa_id=mesa_id).exists():
            messages.error(request, "La mesa seleccionada ya está reservada para esa fecha y hora.")
            return redirect('procesar_reserva')

        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            messages.error(request, "La mesa seleccionada no existe.")
            return redirect('procesar_reserva')

        reserva = Reserva.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            fecha=fecha_reserva,
            hora=hora_reserva,
            personas=personas,
            mesa=mesa
        )

        subject = "Nueva reserva de mesa"
        message = (
            f"Se ha realizado una nueva reserva:\n\n"
            f"Nombre: {nombre}\n"
            f"Correo: {email}\n"
            f"Teléfono: {telefono}\n"
            f"Fecha: {fecha}\n"
            f"Hora: {hora}\n"
            f"Mesa: {mesa.numero}\n"
            f"Número de personas: {personas}\n"
        )

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['pjoseedier@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Reserva realizada y correo enviado con éxito.")
        except Exception as e:
            messages.error(request, f"Reserva realizada, pero hubo un error al enviar el correo: {e}")

        return redirect('procesar_reserva')  # O redirigir a 'reservas'

    return render(request, 'reservas.html', {'mesas': mesas})


def obtener_mesas_disponibles(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    reservas = Reserva.objects.filter(fecha=fecha, hora=hora)
    mesas_reservadas = reservas.values_list('mesa_id', flat=True)
    mesas = Mesa.objects.all()
    mesas_disponibles = []
    for mesa in mesas:
        mesas_disponibles.append({
            'id': mesa.id,
            'numero': mesa.numero,
            'disponible': mesa.id not in mesas_reservadas
        })
    return JsonResponse({'mesas_disponibles': mesas_disponibles})

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def restablecer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/cambiar_contrasena/{uid}/{token}/")
            send_mail(
                'Restablecer contraseña',
                f'Haz clic en el siguiente en enlace para restablecer tu contraseña {enlace}',
                'pjoseedier@gmail.com',
                [email], 
                fail_silently=False
            )
            messages.success(request, "Se ah enviado un enlace de restablecimiento de contraseña a su correo")
            return redirect('iniciar')
        else:
            messages.success(request, "No se encontro algun usuario registrado con ese correo")
        return redirect('restablecer')
    return render(request, 'email_restablecer.html')

def cambiar_contrasena(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contrasena = request.POST.get("password")
            
            if not nueva_contrasena:
                messages.error(request, "La contraseña no puede estar vacía")
                return render(request, "email_contrasena.html")
                
            
            user.set_password(nueva_contrasena)
            user.save()
            
            return redirect('confirmacion_contrasena')
        
        return render(request, "email_contrasena.html")
    return redirect("iniciar")

def confirmacion_contrasena(request):
    return render(request, "cambiar_contrasena.html")


