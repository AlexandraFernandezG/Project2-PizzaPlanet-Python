#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    return render(request, 'pizzaplanet/inicio.html')

def catalogo(request):
    return render(request, 'pizzaplanet/catalogo.html')

def pedidos(request):
    return render(request, 'pizzaplanet/pedidos.html')
