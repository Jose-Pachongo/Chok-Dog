from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
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
    return render(request, 'contactenos.html')
@csrf_protect
def regis(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'regis.html', {'error': 'El nombre de usuario ya está en uso. Prueba con otro.'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'regis.html', {'error': 'El correo electrónico ya está en uso. Prueba con otro.'})

       
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.phone_number = phone 
        user.address = address 
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"{user.first_name} Bienvenido a Chock Dog, Tu cuenta ha sido creada correctamente." )
            return render(request, 'pagina.html')  

    return render(request, 'regis.html')

@csrf_protect
def iniciar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
    
        user = authenticate(request,  username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request,"{user.first_name} Bienvenido a Chock Dog,  has iniciado correctamente." )
            return redirect('pagina') 
        else:
            
            return render(request, 'iniciar.html', {'error': 'Usuario o contraseña incorrectos'})
        
    return render(request, 'iniciar.html')

def pagina(request):
    return render(request, 'pagina.html')

def productos(request):
    return render(request, 'productos.html')

def carrito(request):
    return render(request, 'carrito.html')

def perfil(request):
    return render(request, 'perfil.html')

def logout_request(request):
    logout(request)
    messages.info(request, "tu sesión se ha cerrado correctamente")
    return redirect("home")

@login_required
def perfil_view(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.bio = request.POST.get('bio')

            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']

            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
        except Exception as e:
            messages.error(request, 'Error al actualizar el perfil.')

    return render(request, 'perfil.html')