from django.shortcuts import render, redirect  


# Create your views here.
def home(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def servicios(request):
    return render(request, 'servicios.html')

def contactenos(request):
    return render(request, 'contactenos.html')

def iniciar(request):
        return render(request, 'iniciar.html')

def regis(request):
    return render(request, 'regis.html')

def pagina(request):
    return render(request, 'pagina.html')
