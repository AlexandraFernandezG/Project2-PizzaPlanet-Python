#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida, Cliente, Pedido, Pizza, Ingrediente_pizza,Bebida_pedido,Delivery
from django.http import HttpResponse
import datetime

#Funcion que redirecciona al inicio de la aplicacion
def inicio(request):
    return render(request, 'pizzaplanet/inicio.html')

#Funcion que redirecciona al formulario de pedidos de la aplicacion
def pedidos(request):
    '''Se guardan los tamaños, ingredientes, bebidas registrados en la base de datos para 
       pasarlos a la vista por el contexto y mostrarlos en el formulario
    '''
    tamanos = Tamano.objects.all()      
    ingredientes = Ingrediente.objects.all()
    bebidas = Bebida.objects.all()
    cantPedidos = Pedido.objects.count() + 1    #Se obtiene el numero del pedido a realizarse

    ingredientes_temp = []
    bebidas_temp = []
    tamanos_temp = []

    #Se guardan en una lista los tamaños, bebidas e ingredientes para pasarlas por el contexto
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

#Funcion que crea los objetos asociados al pedido y genera los datos para mostrar la factura final
def confirmacion(request):
    nombre_ingredientes = []
    nombre_bebidas = []
    
    #Se obtiene la lista de los ingredientes y bebidas seleccionados por el usuario
    lista_ingredientes=request.GET.getlist("ingredientes")
    print(lista_ingredientes)

    lista_bebidas=request.GET.getlist("bebidas")
    print(lista_bebidas)

    #Verifica mediante la cedula que el cliente exista en la base de datos
    try:
        existe_cliente=str(Cliente.objects.get(cedula=str(request.GET['cedula'])))
    except Cliente.DoesNotExist:
        existe_cliente=None

    #Si el cliente no existe, se registra en la base de datos
    if(existe_cliente==None):
        cliente_nuevo=Cliente(nombre=request.GET['nombre'], cedula=request.GET['cedula'])
        cliente_nuevo.save()
        print(cliente_nuevo.id)
    else:  #Si el cliente si existe, lo busca y lo guarda en una variable
        cliente_nuevo= Cliente.objects.get(cedula=str(request.GET['cedula']))

   #Crea el pedido asignandole el cliente, fecha actual y total en 0 momentaneamente

    pedido_actual = Pedido(cliente=cliente_nuevo, fecha=datetime.datetime.now(), total=0)
    pedido_actual.save()

    #Busca el tamaño de la pizza y lo guarda
    tamano_pizza = Tamano.objects.get(tipo=str(request.GET['tmo']))

    #Verifica si la pizza es simple(no tiene ingredientes adicionales
    #Se crea la pizza asociada al pedido asociandole el pedido y tamaño. Tambien se le pone un precio en base al tamaño seleccionado
    #Si no tiene ingredientes, el atributo simple sera "true" de lo contrario sera "false"
    if(int(len(lista_ingredientes))==0):
        pizza_pedido = Pizza(simple=True, tamano_id=tamano_pizza, pedido = pedido_actual, precio = tamano_pizza.precio)
    else: 
        pizza_pedido = Pizza(simple=False, tamano_id=tamano_pizza, pedido = pedido_actual, precio = tamano_pizza.precio)
   
    pizza_pedido.save()

   #Se crean los registros en la tabla Ingrediente_pizza
   
    for i in lista_ingredientes:

        pizza_ingredientes = Ingrediente_pizza(pizza=pizza_pedido,ingrediente=Ingrediente.objects.get(id=i))
        pizza_ingredientes.save()

    #Se crean los registros en la tabla Bebida_pedido

    for i in lista_bebidas:
        bebida_pedido = Bebida_pedido(pedido=pedido_actual,bebida=Bebida.objects.get(id=i))
        bebida_pedido.save()

   #Se recorre la lista de ingredientes para añadir el monto adicional al precio de la pizza

    for i in lista_ingredientes:
        pizza_pedido.precio = pizza_pedido.precio + Ingrediente.objects.get(id=i).precio
        pizza_pedido.save()

   #Se guarda la direccion del delivery

    zona = str(request.GET['zona'])
    direccion_delivery = str(request.GET['direccion'])
    direccion_completa = zona + ' ' +direccion_delivery

    #Se verifica si el usuario pidio delivery
    if(zona!="Sin delivery"):
        delivery_pedido = Delivery(direccion=direccion_completa, precio=5)
        delivery_pedido.save()
        con_delivery=True
    else: 
        delivery_pedido = Delivery(direccion=None, precio=None)
        con_delivery=False

   #Se actualiza en precio del pedido tomando el cuenta el monto final de la pizza, bebidas y delivery

    pedido_actual.total = pizza_pedido.precio

    for i in lista_bebidas:
        pedido_actual.total = pedido_actual.total + Bebida.objects.get(id=i).precio

    if(con_delivery):
        pedido_actual.delivery=delivery_pedido
        pedido_actual.total = pedido_actual.total + delivery_pedido.precio
    else: 
        pass

    pedido_actual.save()

    #Se guardan los nombres de los ingredientes y bebidas para mostrarlos en la factura

    #Nombre ingredientes
    for i in lista_ingredientes:
        nombre_ingredientes.append(Ingrediente.objects.get(id=i))
    
    #Nombre bebidas
    for i in lista_bebidas:
        nombre_bebidas.append(Bebida.objects.get(id=i))

    cantPedidos = Pedido.objects.count()

    context = {
        "cliente_temp": cliente_nuevo,
        "pedido_temp": pedido_actual,
        "cantPizzas_temp": 1,
        "tamano_temp": tamano_pizza,
        "ingredientes_temp": nombre_ingredientes,
        "bebidas_temp": nombre_bebidas,
        "delivery_temp": con_delivery,
        "zona_temp": zona,
        "direccion_temp":  direccion_delivery,
        "precioDelivery_temp":  5,
        "cantPedidos": cantPedidos
    }

    return render(request, 'pizzaplanet/confirmacion.html', context) #Redirecciona a la pagina de confirmacion del pedido

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
                    SELECT Pedido.id as id, Pedido.total as Total, Pedido.fecha as Fecha
                    FROM pizzaplanet_pedido as Pedido;
                 ''' 
    results = Pedido.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventaspordia.html', {'resultado': results})

# Obtiene un listado de las ventas por tamaño de pizza
def ventasTamano(request):
    
    raw_query =  '''
                    SELECT Tamano.id as id, Tamano.tipo as Tamano, SUM(Pizza.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_tamano as Tamano
                    WHERE Tamano.id=Pizza.tamano_id_id and Tamano.tipo="Grande"
                    UNION
                    SELECT Tamano.id as id, Tamano.tipo as Tamano, SUM(Pizza.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_tamano as Tamano
                    WHERE Tamano.id=Pizza.tamano_id_id and Tamano.tipo="Mediana"
                    UNION
                    SELECT Tamano.id as id, Tamano.tipo as Tamano, SUM(Pizza.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_tamano as Tamano
                    WHERE Tamano.id=Pizza.tamano_id_id and Tamano.tipo="Personal"
                    ORDER BY Tamano
                 ''' 
    results = Tamano.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasportamano.html', {'resultado': results})

# Obtiene un listado de las ventas por ingredientes adicionales de pizza
def ventasIngrediente(request):
    
    raw_query = '''SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Pimenton"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Pepperoni"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Salchichon"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Aceitunas"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Champiñones"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Doble queso"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Pepperoni"
                    UNION
                    SELECT Ingrediente.id as id, Ingrediente.nombre as Ingrediente, sum(Ingrediente.precio) as Total
                    FROM pizzaplanet_pizza as Pizza, pizzaplanet_ingrediente as Ingrediente, pizzaplanet_ingrediente_pizza IP
                    WHERE Pizza.id=IP.pizza_id and Ingrediente.id=IP.ingrediente_id and Ingrediente.nombre="Jamon"
                    ORDER BY Ingrediente;
                 ''' 
    results = Ingrediente.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasporingrediente.html', {'resultado': results})

# Obtener un listado de las ventas por clientes (ordenado de mayor a menor)
def ventasCliente(request):
    
    raw_query = '''select Cliente.id, Pedido.cliente_id as Pedido, cliente.nombre as Nombre, count(Pedido.cliente_id) as Total
                    from pizzaplanet_pedido as Pedido, pizzaplanet_cliente as Cliente
                    WHERE Cliente.id=Pedido.cliente_id
                    group by Nombre, Pedido
                ''' 
    results = Cliente.objects.raw(raw_query)
    return render(request, 'pizzaplanet/ventasporclientes.html', {'resultado': results})