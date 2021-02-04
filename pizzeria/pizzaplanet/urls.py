from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('pedidos', views.pedidos, name="pedidos"),
    path('confirmacion', views.confirmacion, name="confirmacion"),
    path('ventasGenerales', views.ventasGenerales, name="ventasGenerales"),
    path('ventasDia', views.ventasDia, name="ventasDia"),
    path('ventasTamano', views.ventasTamano, name="ventasTamano"),
    path('ventasIngrediente', views.ventasIngrediente, name="ventasIngrediente"),
    path('ventasCliente', views. ventasCliente, name="ventasCliente"),

]