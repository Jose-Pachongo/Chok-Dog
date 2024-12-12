from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')
def nosotros(request):
    return render(request,'nosotros.html')
def servicios(request):
    return render(request,'servicios.html')
def contactenos(request):
    return render(request,'contactenos.html')
def login(request):
    return render(request,'login.html')
