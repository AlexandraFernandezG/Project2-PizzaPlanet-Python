from django.contrib import admin

# Register your models here.

from .models import Cliente, Delivery, Bebida, Pedido, Pago, Calificacion, Tamaño, Ingrediente, Pizza, Ingrediente_pizza

admin.site.register(Cliente)
admin.site.register(Delivery)
admin.site.register(Bebida)
admin.site.register(Pedido)
admin.site.register(Pago)
admin.site.register(Calificacion)
admin.site.register(Tamaño)
admin.site.register(Ingrediente)
admin.site.register(Pizza)
admin.site.register(Ingrediente_pizza)