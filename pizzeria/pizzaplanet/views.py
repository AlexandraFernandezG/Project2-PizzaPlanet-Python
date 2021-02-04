#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida, Pedido
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
    cantPedidos = Pedido.objects.count() + 1

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
        "numero_pedidos": cantPedidos
    }
    return render(request, 'pizzaplanet/pedidos.html', context)

def confirmacion(request):
    pedido = 1201
    cantPizzas = 3
    delivery = False
    zona = None
    direccion = None
    
    #hacer select de los ingredientes con nombre y precio
    #hacer select de las bebidas con nombre y precio
    #hacer select de la cantidad de pizzas del pedido
    #saber como tengo el numero del pedido
    #zona deberia ser un objeto para que me diga la zona y el precio
    try:
        if(request.GET["delivery"] == 'True'):
            delivery = request.GET["delivery"]
            zona = request.GET["zona"]
            direccion = request.GET["direccion"]
    except:
        print('error')


    context = {
        "nombre_temp": request.GET["firstName"],
        "cedula_temp": request.GET["cedula"],
        "pedido_temp": pedido,
        "cantPizzas_temp": cantPizzas,
        "ingredientes_temp": request.GET.getlist("ingredientes"),
        "bebidas_temp": request.GET.getlist("bebidas"),
        "delivery_temp": delivery,
        "zona_temp": zona,
        "direccion_temp":  direccion,
    }
    return render(request, 'pizzaplanet/confirmacion.html', context)




def confirmacion(request):
    pedido = 1201
    cantPizzas = 3
    delivery = False
    zona = None
    direccion = None
    
    #hacer select de los ingredientes con nombre y precio
    #hacer select de las bebidas con nombre y precio
    #hacer select de la cantidad de pizzas del pedido
    #saber como tengo el numero del pedido
    #zona deberia ser un objeto para que me diga la zona y el precio
    try:
        if(request.GET["delivery"] == 'True'):
            delivery = request.GET["delivery"]
            zona = request.GET["zona"]
            direccion = request.GET["direccion"]
    except:
        print('error')


    context = {
        "nombre_temp": request.GET["firstName"],
        "cedula_temp": request.GET["cedula"],
        "pedido_temp": pedido,
        "cantPizzas_temp": cantPizzas,
        "ingredientes_temp": request.GET.getlist("ingredientes"),
        "bebidas_temp": request.GET.getlist("bebidas"),
        "delivery_temp": delivery,
        "zona_temp": zona,
        "direccion_temp":  direccion,
    }
    return render(request, 'pizzaplanet/confirmacion.html', context)
