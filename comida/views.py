from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')
def nosotros(request):
    return render(request,'nosotros.html')
def servicios(request):
    return render(request,'servicios.html')
def contactenos(request):
    return render(request,'contactenos.html')
def iniciar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página deseada
        else:
            messages.error(request, 'Credenciales incorrectas. Por favor, regístrese si no tiene cuenta.')
            return redirect('iniciar')
    else:
        return render(request, 'iniciar.html')
def regis(request):
    return render(request,'regis.html')
def pagina(request):
    return render(request, 'pagina.html')
