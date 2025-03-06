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
from django.contrib.auth.tokens import default_token_generator



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
                send_mail(subject, message, settings.EMAIL_HOST_USER, ['chokdog77@gmail.com'])
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
    return render(request, 'productos.html', {'productos': productos})
    

def carrito(request):
    return render(request, 'carrito.html')

def perfil(request):
    return render(request, 'perfil.html')

def logout_request(request):
    logout(request)
    return redirect("home")


    return render(request, 'perfil.html')


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, ProfileForm, ChangePasswordForm

@login_required
def profile(request):
    user_form = UserProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    password_form = ChangePasswordForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = UserProfileForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
        
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('profile')

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })


#reservas


from datetime import datetime, timedelta

from datetime import datetime, timedelta

def reservas(request):
    mesas = Mesa.objects.all()

    if request.method == "POST":
        nombre = request.POST["nombre"]
        email = request.POST["email"]
        telefono = request.POST["telefono"]
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        mesa_id = request.POST["mesa"]
        personas = int(request.POST["personas"])

        try:
            fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_reserva = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            messages.error(request, "Formato incorrecto de fecha u hora.")
            return redirect('reservas')

        # Validar que la fecha no sea pasada
        if fecha_reserva < datetime.now().date():
            messages.error(request, "No puedes seleccionar una fecha pasada.")
            return redirect('reservas')
        
        if not (datetime.strptime('17:00', '%H:%M').time() <= hora_reserva <= datetime.strptime('23:00', '%H:%M').time()):
            messages.error(request, "La hora debe estar entre las 17:00 y las 23:00.")
            return redirect('reservas')
        
        dt_reserva = datetime.combine(fecha_reserva, hora_reserva)
        dt_inicio = dt_reserva - timedelta(minutes=30)
        dt_fin = dt_reserva + timedelta(minutes=30)

        # Verificar si la mesa ya está reservada en ese horario
        if Reserva.objects.filter(
            fecha=fecha,
            mesa_id=mesa_id,
            hora__gte=dt_inicio.time(),
            hora__lte=dt_fin.time()
        ).exists():
            messages.error(request, "Lo siento, esta mesa ya está reservada en ese horario.")
            return redirect("reservas")

        # Guardar la reserva
        reserva = Reserva.objects.create(
            nombre=nombre, email=email, telefono=telefono,
            fecha=fecha, hora=hora, mesa_id=mesa_id, personas=personas
        )

        
        subject_user = "Confirmación de Reserva - Chokdog"
        message_user = (
            f"Hola {nombre},\n\n"
            f"Tu reserva ha sido confirmada:\n"
            f"- 📅 Fecha: {fecha}\n"
            f"- ⏰ Hora: {hora}\n"
            f"- 🍽 Mesa: {reserva.mesa.numero}\n"
            f"- 👥 Número de personas: {personas}\n\n"
            f"Si necesitas cancelar o modificar tu reserva, contáctanos.\n"
            f"¡Gracias por elegirnos!\n\n"
            f"Atentamente,\n"
            f"Chokdog"
        )
        send_mail(subject_user, message_user, settings.EMAIL_HOST_USER, [email])

       
        subject_admin = "Nueva Reserva Recibida"
        message_admin = (
            f"📌 Nueva reserva registrada en Chokdog:\n\n"
            f"- Cliente: {nombre}\n"
            f"- 📧 Correo: {email}\n"
            f"- 📞 Teléfono: {telefono}\n"
            f"- 📅 Fecha: {fecha}\n"
            f"- ⏰ Hora: {hora}\n"
            f"- 🍽 Mesa: {reserva.mesa.numero}\n"
            f"- 👥 Número de personas: {personas}\n\n"
            f"✅ Verificar disponibilidad y preparar el servicio.\n"
            f"Gracias."
        )
        send_mail(subject_admin, message_admin, settings.EMAIL_HOST_USER, ["chokdog77@gmail.com"])

        messages.success(request, "¡Tu reserva fue realizada con éxito! Se ha enviado un correo con los detalles.")
        return redirect("reservas")

    return render(request, "reservas.html", {"mesas": mesas})


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
                ['chokdog77@gmail.com'],
                fail_silently=False,
            )
            
            send_mail(
                'Bienvenido a Nuestra Página',
                mensaje_usuario,
                'chokdog77@gmail.com',  # Remitente
                [email],  # Usuario registrado
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

    try:
        fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_reserva = datetime.strptime(hora, '%H:%M').time()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha u hora incorrecto'}, status=400)

    dt_reserva = datetime.combine(fecha_reserva, hora_reserva)
    dt_inicio = dt_reserva - timedelta(minutes=30)
    dt_fin = dt_reserva + timedelta(minutes=30)

    reservas = Reserva.objects.filter(
        fecha=fecha,
        hora__gte=dt_inicio.time(),
        hora__lte=dt_fin.time()
    )
    mesas_reservadas = reservas.values_list('mesa_id', flat=True)

    mesas = Mesa.objects.all()
    mesas_disponibles = [
        {'id': mesa.id, 'numero': mesa.numero, 'disponible': mesa.id not in mesas_reservadas}
        for mesa in mesas
    ]

    return JsonResponse({'mesas_disponibles': mesas_disponibles})

from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str


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
                'chokdog77@gmail.com',
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
            messages.success(request, "Tu contraseña se ha cambiado con éxito.")
            return redirect("cambiar_contrasena", uidb64=uidb64, token=token)  # Recargar la misma página

        return render(request, "email_contrasena.html")
    
    return redirect("iniciar")

def confirmacion_contrasena(request):
    return render(request, "cambiar_contrasena.html")


def pago(request):
    return render(request, 'pago.html')
def pasarela_pago(request):
    carrito = request.session.get('carrito', [])  # Asegúrate de que el carrito está en la sesión
    return render(request, 'pasarela_pago.html', {'carrito': carrito})



from django.shortcuts import render
from .models import Producto

def lista_productos(request):
    productos = Producto.objects.all()  # Obtener productos
    return render(request, "productos.html", {"productos": productos})

import json

from django.http import JsonResponse
from django.shortcuts import render
from .forms import PedidoForm

def pagina_pago(request):
    return render(request, 'pago.html')

def procesar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False) 
            if "comprobante" in request.FILES: 
                pedido.comprobante = request.FILES["comprobante"]
            pedido.save() 

            if isinstance(pedido.productos, str):  
                productos = json.loads(pedido.productos)  
            else:  
                productos = pedido.productos 

           
            productos_str = "\n".join([
                f"- {p['cantidad']}x {p['nombre']} - ${p['precio']}" +
                (f" (Sabor: {p['sabor']})" if p.get('sabor') else "") +
                (f" [Ingredientes: {', '.join(p['ingredientes'])}]" if p.get('ingredientes') else "")
                for p in productos
            ])

           
            comprobante_url = request.build_absolute_uri(pedido.comprobante.url) if pedido.comprobante else "No adjunto"

            asunto_usuario = "Confirmación de tu Pedido - Chokdog"
            mensaje_usuario = f"""
            ¡Hola {pedido.nombre}!

            Gracias por tu pedido en Chokdog. Aquí están los detalles:


            Método de pago: {pedido.metodo_pago}
            Total: ${pedido.total}

            Productos:
            {productos_str}


            Estamos procesando tu pedido y nos pondremos en contacto pronto. 
            

            ¡Gracias por confiar en nosotros!



            -- El equipo de Chokdog 🐶🍔
            """
            send_mail(asunto_usuario, mensaje_usuario, 'chokdog77@gmail.com', [pedido.email])

            # 🔹 Correo para el administrador de Chokdog
            asunto_admin = f"Nuevo Pedido Recibido de {pedido.nombre}"
            mensaje_admin = f"""
            📢 Nuevo Pedido Recibido

            Cliente: {pedido.nombre}
            Correo: {pedido.email}
            Teléfono: {pedido.telefono}
            Dirección: {pedido.direccion}

            Método de pago: {pedido.metodo_pago}
            Total: ${pedido.total}

            Productos:
            {productos_str}

            📎 Comprobante de pago: {comprobante_url}

            📌 Revisar en el panel de administración.
            """
            send_mail(asunto_admin, mensaje_admin, 'chokdog77@gmail.com', ['chokdog77@gmail.com'])

            return JsonResponse({"mensaje": "Pedido realizado con exito, en su correo podra ver los detalles."}, status=200)
        else:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
    return render(request, 'pago.html')

