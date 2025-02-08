from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model


def home(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def servicios(request):
    return render(request, 'servicios.html')

def contactenos(request):
    return render(request, 'contactenos.html')

def regis(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'iniciar.html', {'error': 'El nombre de usuario ya está en uso. Prueba con otro.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'iniciar.html', {'error': 'el gmail ya está en uso. Prueba con otro.'})
        
        user = User.objects.create_user(username=username, email=email, password=password )
        user.save()
        
        
        # Iniciar sesión automáticamente
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pagina')  
    return render(request, 'regis.html')

def iniciar(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            username = user.username  # Obtener el username real
        except User.DoesNotExist:
            return render(request, 'iniciar.html', {'error': 'Usuario o contraseña incorrectos'})

        # Autenticación con Django
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('pagina')  # Redirige a la página
        else:
            # Si las credenciales son incorrectas
            return render(request, 'iniciar.html', {'error': 'Usuario o contraseña incorrectos'})
    
    return render(request, 'iniciar.html')

def pagina(request):
    return render(request, 'pagina.html')
