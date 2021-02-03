#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida, Cliente, Pedido, Pizza, Ingrediente_pizza
from django.http import HttpResponse
import datetime

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
    lista_ingredientes=request.GET.getlist("ingredientes")
    print(lista_ingredientes)

    try:
        test=str(Cliente.objects.get(cedula=str(request.GET['cedula'])))
    except Cliente.DoesNotExist:
        test=None

   #Cliente

    if(test==None):
        cliente_nuevo=Cliente(nombre=request.GET['nombre'], cedula=request.GET['cedula'])
        cliente_nuevo.save()
        print(cliente_nuevo.id)
    else:  
        cliente_nuevo= Cliente.objects.get(cedula=str(request.GET['cedula']))

   #Pedido

    pedido_actual = Pedido(cliente=cliente_nuevo, fecha=datetime.datetime.now(), total=0)
    pedido_actual.save()

   #Pizza

    tamano_pizza = Tamano.objects.get(tipo=str(request.GET['tmo']))
    pizza_pedido = Pizza(simple=True, tamano_id=tamano_pizza, pedido = pedido_actual, precio = tamano_pizza.precio)
    pizza_pedido.save()

   #Ingrediente_pizza
   
    for i in lista_ingredientes:

        pizza_ingredientes = Ingrediente_pizza(pizza=pizza_pedido,ingrediente=Ingrediente.objects.get(id=i))
        pizza_ingredientes.save()

   #Actualizar precio pizza 

    for i in lista_ingredientes:
        pizza_pedido.precio = pizza_pedido.precio + Ingrediente.objects.get(id=i).precio
        pizza_pedido.save()

   #Actualizar precio pedido

    pedido_actual.total = pizza_pedido.precio

    message = "Pedido realizado exitosamente."

    return HttpResponse(message)
