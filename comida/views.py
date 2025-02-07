from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



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
        
        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        # Iniciar sesión automáticamente
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pagina')  
    return render(request, 'regis.html')

def iniciar(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['clave']
        
        # Autenticación con Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('pagina')  # Redirige a la página
        else:
            # Si las credenciales son incorrectas
            return render(request, 'iniciar.html', {'error': 'Usuario o contraseña incorrectos'})
    
    return render(request, 'iniciar.html')

def pagina(request):
    return render(request, 'pagina.html')
