#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida
from django.http import HttpResponse

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

    #pizzas = [ {}, {}]

    for ingrediente in ingredientes:
        ingredientes_temp.append({"id": ingrediente.id, "nombre": ingrediente.nombre, "precio": ingrediente.precio})
  
    for tamano in tamanos:
        tamanos_temp.append({"id": tamano.id, "tipo": tamano.tipo, "precio": tamano.precio})
  
    for bebida in bebidas:
        bebidas_temp.append({"id": bebida.id, "tipo": bebida.tipo, "precio": bebida.precio})

    context = {
        "tamanos_temp": tamanos_temp,
        "ingredientes_temp": ingredientes_temp,
        "bebidas_temp" : bebidas_temp,
    }
    return render(request, 'pizzaplanet/pedidos.html', context)

def enviar(request):
    nombre=request.GET["firstName"]
    ingrediente=request.GET["ingredientes"]

    message = request.GET

    print(message)
    print("Pedido listo. Cliente: "+nombre)
    return HttpResponse(message)
