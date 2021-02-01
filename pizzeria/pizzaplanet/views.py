#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida

'''  
context = { 
    'latest_question_list': latest_question_list,     Aqui pongo datos para mandarlo a template
}
'''

def inicio(request):
    return render(request, 'pizzaplanet/inicio.html')

def pedidos(request):
    tamanos = Tamano.objects.all()
    ingredientes = Ingrediente.objects.all()
    bebidas = Bebida.objects.all()

    ingredientes_temp = []
    bebidas_temp = []
    tamanos_temp = []

    for ingrediente in ingredientes:
        ingredientes_temp.append({"id": ingrediente.id, "nombre": ingrediente.nombre, "precio": ingrediente.precio})
  
    for tamano in tamanos:
        tamanos_temp.append({"id": tamano.id, "tipo": tamano.tipo, "precio": tamano.precio})
  
    for bebida in bebidas:
        bebidas_temp.append({"id": bebida.id, "tipo": bebida.tipo, "precio": bebida.precio})

    context = {
        "tamanos": tamanos,
        "ingredientes": ingredientes,
        "bebida" : bebida,
    }
    return render(request, 'pizzaplanet/pedidos.html', context)
