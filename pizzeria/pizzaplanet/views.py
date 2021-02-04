#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida, Cliente, Pedido, Pizza, Ingrediente_pizza,Bebida_pedido,Delivery
from django.http import HttpResponse
import datetime


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
    nombre_ingredientes = []
    nombre_bebidas = []
    
    lista_ingredientes=request.GET.getlist("ingredientes")
    print(lista_ingredientes)

    lista_bebidas=request.GET.getlist("bebidas")
    print(lista_bebidas)

    try:
        existe_cliente=str(Cliente.objects.get(cedula=str(request.GET['cedula'])))
    except Cliente.DoesNotExist:
        existe_cliente=None

   #Cliente

    if(existe_cliente==None):
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
    ###arreglar
    if(int(len(lista_ingredientes))==0):
        pizza_pedido = Pizza(simple=True, tamano_id=tamano_pizza, pedido = pedido_actual, precio = tamano_pizza.precio)
    else: 
        pizza_pedido = Pizza(simple=False, tamano_id=tamano_pizza, pedido = pedido_actual, precio = tamano_pizza.precio)
   
    pizza_pedido.save()

   #Ingrediente_pizza
   
    for i in lista_ingredientes:

        pizza_ingredientes = Ingrediente_pizza(pizza=pizza_pedido,ingrediente=Ingrediente.objects.get(id=i))
        pizza_ingredientes.save()

     #Bebida_pedido

    for i in lista_bebidas:
        bebida_pedido = Bebida_pedido(pedido=pedido_actual,bebida=Bebida.objects.get(id=i))
        bebida_pedido.save()

   #Actualizar precio pizza 

    for i in lista_ingredientes:
        pizza_pedido.precio = pizza_pedido.precio + Ingrediente.objects.get(id=i).precio
        pizza_pedido.save()

   #Delivery

    zona = str(request.GET['zona'])
    direccion_delivery = str(request.GET['direccion'])
    direccion_completa = zona + ' ' +direccion_delivery

    if(zona!="Sin delivery"):
        delivery_pedido = Delivery(direccion=direccion_completa, precio=5)
        delivery_pedido.save()
        con_delivery=True
    else: 
        delivery_pedido = Delivery(direccion=None, precio=None)
        con_delivery=False

   #Actualizar precio pedido

    pedido_actual.total = pizza_pedido.precio

    for i in lista_bebidas:
        pedido_actual.total = pedido_actual.total + Bebida.objects.get(id=i).precio

    if(con_delivery):
        pedido_actual.delivery=delivery_pedido
        pedido_actual.total = pedido_actual.total + delivery_pedido.precio
    else: 
        pass

    pedido_actual.save()

    message = "Pedido realizado exitosamente."
    print(message)

    #Nombre ingredientes
    for i in lista_ingredientes:
        nombre_ingredientes.append(Ingrediente.objects.get(id=i))
    
    #Nombre ingredientes
    for i in lista_bebidas:
        nombre_bebidas.append(Bebida.objects.get(id=i))

    print(nombre_ingredientes)
    print(nombre_bebidas)

    context = {
        "cliente_temp": cliente_nuevo,
        "pedido_temp": pedido_actual,
        "cantPizzas_temp": 3,
        "tamano_temp": tamano_pizza,
        "ingredientes_temp": nombre_ingredientes,
        "bebidas_temp": nombre_bebidas,
        "delivery_temp": con_delivery,
        "zona_temp": zona,
        "direccion_temp":  direccion_delivery,
        "precioDelivery_temp":  5,
    }

    return render(request, 'pizzaplanet/confirmacion.html', context)

#######################################################################
# Reportes de Ventas
#######################################################################


# Obtiene un listado de las ventas realizadas (general)
def ventasGenerales(request):
    
    raw_query = '''
                    SELECT Pedido.id as id, Pedido.total as Total, Pedido.fecha as Fecha,  Cliente.nombre as Nombre
                    FROM pizzaplanet_pedido as Pedido, pizzaplanet_cliente as Cliente
                    WHERE Cliente.id=Pedido.cliente_id 
                 ''' 
    results = Pedido.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasgenerales.html', {'resultado': results})


# Obtiene un listado de las ventas totales por día
def ventasDia(request):
    
    raw_query = '''
                    SELECT Pedido.id as id, SUM(Pedido.total) as Total, Pedido.fecha as Fecha
                    FROM pizzaplanet_pedido as Pedido 
                    ORDER BY Fecha;
                 ''' 
    results = Pedido.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventaspordia.html', {'resultado': results})

# Obtiene un listado de las ventas por tamaño de pizza
def ventasTamano(request):
    
    raw_query = '''
                    SELECT Tamano.id as id, Tamano.tipo as Tamano, sum(Tamano.precio)
                    FROM pizzaplanet_pedido as Pedido, pizzaplanet_pizza as Pizza, pizzaplanet_tamano as Tamano
                    WHERE Pedido.id= Pizza.pedido_id and Pizza.id=Pizza.tamano_id_id 
                    ORDER BY Tamano;
                 ''' 
    results = Pedido.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasportamano.html', {'resultado': results})

# Obtiene un listado de las ventas por ingredientes adicionales de pizza
def ventasIngrediente(request):
    
    raw_query = '''SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                   FROM pizzaplanet_pedido as Pedido, pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                   WHERE Pedido.id= Pizza.pedido_id and Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id
                   ORDER BY Ingrediente;
                 ''' 
    results = Ingrediente.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasporingrediente.html', {'resultado': results})

# Obtener un listado de las ventas por clientes (ordenado de mayor a menor)
def ventasCliente(request):
    
    raw_query = '''SELECT Cliente.id as id, sum(Pedido.total) as Total, Cliente.nombre as Nombre
                   FROM pizzaplanet_pedido as Pedido, pizzaplanet_cliente as Cliente
                   WHERE Cliente.id=Pedido.cliente_id 
                   ORDER BY Pedido.total desc;
                 ''' 
    results = Cliente.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasporclientes.html', {'resultado': results})