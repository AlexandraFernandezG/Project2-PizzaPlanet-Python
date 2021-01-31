from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('catalogo', views.catalogo, name="catalogo"),
    path('pedidos', views.pedidos, name="pedidos"),   #En views busca funcion index. Ya tengo ruta para llegarle a index
]