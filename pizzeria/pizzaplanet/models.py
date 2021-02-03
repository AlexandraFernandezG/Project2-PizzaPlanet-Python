from django.db import models

# Create your models here.
#Aqui van las tablas de BD

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    cedula =  models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Delivery(models.Model):
    direccion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

class Bebida(models.Model):
    tipo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.tipo

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    fecha = models.DateTimeField('Fecha pedido', null=True)

class Pago(models.Model):
    tipo_pago = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=6, decimal_places=2)

class Calificacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=500, null=True)
    puntuacion = models.IntegerField(default=0)

    def __str__(self):
        return self.comentario

class Tamano(models.Model):
    tipo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.tipo


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nombre


class Pizza(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    tamano_id = models.ForeignKey(Tamano, on_delete=models.CASCADE)
    simple = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

class Ingrediente_pizza(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)


