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


# Esto es correcto


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


@login_required(login_url='home')
def pagina(request):
    return render(request, 'pagina.html')

@login_required(login_url='home')
def productos(request):
    products = Product.objects.all()
    return render(request, 'productos.html', {'productos': productos})
    
@login_required(login_url='home')
def carrito(request):
    return render(request, 'carrito.html')
@login_required(login_url='home')
def perfil(request):
    return render(request, 'perfil.html')

def logout_request(request):
    logout(request)
    return redirect("home")


    return render(request, 'perfil.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile  # Asegúrate de importar tu modelo de perfil
from django.contrib.auth.models import User

@login_required(login_url='home')
def profile_view(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_number = request.POST.get("phone_number", profile.phone_number)
        profile.address = request.POST.get("address", profile.address)
        
        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]


        user.save()
        profile.save()

        messages.success(request, "Perfil actualizado correctamente")
        return redirect("perfil")  # Ajusta esto si tu URL de perfil tiene otro nombre

    return render(request, "perfil.html")


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def eliminar_foto(request):
    if request.method == "POST":
        user = request.user
        if user.profile.profile_picture:
            user.profile.profile_picture.delete()
            user.profile.profile_picture = None
            user.profile.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No hay foto para eliminar."})
    return JsonResponse({"success": False, "error": "Método no permitido."})

#reservas

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/home/')  # Redirige a la página de inicio de sesión
# def reservas(request):
#     return render(request, 'reservas.html')





from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Mesa, Reserva

def enviar_correo(request, destinatario, asunto, mensaje):
    try:
        send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [destinatario])
    except Exception as e:
        messages.error(request, f"Error al enviar el correo: {e}")

@login_required(login_url='home')
def reservas(request):
    mesas_disponibles = Mesa.objects.all()
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        mesa_id = request.POST.get("mesa")
        personas = request.POST.get("personas")
        
        try:
            fecha_reserva = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_reserva = datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            messages.error(request, "Formato incorrecto de fecha u hora.")
            return redirect("reservas")
        
        # Validar que la fecha no sea pasada
        if fecha_reserva < datetime.now().date():
            messages.error(request, "No puedes seleccionar una fecha pasada.")
            return redirect("reservas")
        
        # Validar que la hora esté en el rango permitido
        if not (datetime.strptime("17:00", "%H:%M").time() <= hora_reserva <= datetime.strptime("23:00", "%H:%M").time()):
            messages.error(request, "La hora debe estar entre las 17:00 y las 23:00.")
            return redirect("reservas")
        
        # Verificar disponibilidad de la mesa
        dt_reserva = datetime.combine(fecha_reserva, hora_reserva)
        dt_inicio = dt_reserva - timedelta(minutes=30)
        dt_fin = dt_reserva + timedelta(minutes=30)
        
        if Reserva.objects.filter(
            fecha=fecha_reserva,
            mesa_id=mesa_id,
            hora__gte=dt_inicio.time(),
            hora__lte=dt_fin.time(),
            estado__in=["Pendiente", "Confirmada"]  # solo considera reservas activas
        ).exists():

            messages.error(request, "Lo siento, esta mesa ya está reservada en ese horario.")
            return redirect("reservas")
        
        # Crear la reserva
        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            messages.error(request, "La mesa seleccionada no existe.")
            return redirect("reservas")
        
        reserva = Reserva.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            nombre=nombre, email=email, telefono=telefono,
            fecha=fecha_reserva, hora=hora_reserva, mesa=mesa, personas=personas
        )
        
        # Enviar correos
        mensaje_usuario = f"""
        Hola {nombre},
        
        Tu reserva ha sido confirmada:
        📅 Fecha: {fecha}
        ⏰ Hora: {hora}
        🍽 Mesa: {mesa.numero}
        👥 Número de personas: {personas}
        
        Si necesitas cancelar o modificar tu reserva, contáctanos.
        ¡Gracias por elegirnos!
        """
        enviar_correo(email, "Confirmación de Reserva - Chokdog", mensaje_usuario)
        
        mensaje_admin = f"""
        📌 Nueva reserva recibida:
        
        Cliente: {nombre}
        📧 Correo: {email}
        📞 Teléfono: {telefono}
        📅 Fecha: {fecha}
        ⏰ Hora: {hora}
        🍽 Mesa: {mesa.numero}
        👥 Número de personas: {personas}
        """
        enviar_correo("chokdog77@gmail.com", "Nueva Reserva Recibida", mensaje_admin)
        
        messages.success(request, "¡Tu reserva fue realizada con éxito! Se ha enviado un correo con los detalles.")
        return redirect("reservas")
    
    return render(request, "reservas.html", {"mesas": mesas_disponibles})

from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mesa, Reserva  # Asegúrate de importar los modelos correctos

def enviar_correo(destinatario, asunto, mensaje):
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Asegúrate de configurar esto en settings.py
        recipient_list=[destinatario],
        fail_silently=False,
    )


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
            'capacidad': mesa.capacidad,
            'disponible': mesa.id not in mesas_reservadas
        })

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
            messages.success(request, "Se ha enviado un enlace de restablecimiento de contraseña a su correo")
            return redirect('iniciar')
        else:
            messages.error(request, "No se encontro algun usuario registrado con ese correo")
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

@login_required(login_url='home')
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

@login_required(login_url='home')
def pagina_pago(request):
    return render(request, 'pago.html')

def procesar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False) 
            pedido.usuario = request.user if request.user.is_authenticated else None  # Asigna el usuario autenticado
            pedido.save()
            
            # 🔹 Si el pago es contra entrega, no se requiere comprobante
            if request.POST.get("metodo_pago") == "contra_entrega":
                pedido.comprobante = None
            else:
                pedido.comprobante = request.FILES.get("comprobante")

            pedido.save() 

            # Manejar productos correctamente
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

            # 🔹 Enviar correo al usuario
            send_mail(
                "Confirmación de tu Pedido - Chokdog",
                f"Hola {pedido.nombre},\n\nGracias por tu pedido en Chokdog.\n\n"
                f"Método de pago: {pedido.metodo_pago}\n"
                f"Total: ${pedido.total}\n\n"
                f"Productos:\n{productos_str}\n\nEstamos procesando tu pedido.\n\n¡Gracias por confiar en nosotros!",
                "chokdog77@gmail.com",
                [pedido.email]
            )

            # 🔹 Enviar correo al administrador
            send_mail(
                f"Nuevo Pedido Recibido de {pedido.nombre}",
                f"📢 Nuevo Pedido Recibido\n\n"
                f"Cliente: {pedido.nombre}\nCorreo: {pedido.email}\nTeléfono: {pedido.telefono}\nDirección: {pedido.direccion}\n"
                f"Método de pago: {pedido.metodo_pago}\nTotal: ${pedido.total}\n\nProductos:\n{productos_str}\n\n"
                f"📎 Comprobante: {comprobante_url}\n\n📌 Revisar en el panel de administración.",
                "chokdog77@gmail.com",
                ["chokdog77@gmail.com"]
            )

            return JsonResponse({"mensaje": "Pedido realizado con éxito. Revisa tu correo para más detalles."}, status=200)

        else:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

    return render(request, 'pago.html')


@login_required(login_url='home')
def manual(request):
    return render(request, 'manual.html')

from django.shortcuts import render
from .models import Pedido, Reserva  # Importa el modelo

import json
from django.shortcuts import render
from .models import Pedido, Reserva

def historial(request):
    pedidos = []
    reservas = []

    if request.user.is_authenticated:
        # Buscar por usuario en lugar de solo email
        pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
        reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha')

        for pedido in pedidos:
            pedido.estado_display = pedido.get_estado_display()
            pedido.productos = json.loads(pedido.productos) if isinstance(pedido.productos, str) else pedido.productos

    return render(request, "historial.html", {"pedidos": pedidos, "reservas": reservas})




from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from comida.models import Reserva

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    return JsonResponse({"mensaje": "Reserva eliminada correctamente"})



from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from comida.models import Pedido, Reserva

def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if pedido.estado == "Pendiente":  # Solo cancelar si está pendiente
        pedido.estado = "Cancelado"
        pedido.save()

        # Obtener datos del usuario
        usuario_nombre = f"{request.user.first_name} {request.user.last_name}".strip()
        usuario_email = request.user.email

        # Enviar correo al administrador
        send_mail(
            subject="Pedido Cancelado",
            message=f"El usuario {usuario_nombre} ({usuario_email}) ha cancelado su pedido con ID {pedido.id}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['chokdog77@gmail.com'],  # Cambia esto si el correo es otro
            fail_silently=False,
        )

        messages.success(request, "El pedido ha sido cancelado correctamente.")
    else:
        messages.error(request, "No se puede cancelar este pedido.")

    return redirect('historial')

def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if reserva.estado == "Pendiente":  # Solo cancelar si está pendiente
        reserva.estado = "Cancelado"
        reserva.save()

        # Obtener datos del usuario
        usuario_nombre = f"{request.user.first_name} {request.user.last_name}".strip()
        usuario_email = request.user.email

        # Enviar correo al administrador
        send_mail(
            subject="Reserva Cancelada",
            message=f"El usuario {usuario_nombre} ({usuario_email}) ha cancelado su reserva con ID {reserva.id}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['chokdog77@gmail.com'],  # Cambia esto si el correo es otro
            fail_silently=False,
        )

        messages.success(request, "La reserva ha sido cancelada correctamente.")
    else:
        messages.error(request, "No se puede cancelar esta reserva.")

    return redirect('historial')



