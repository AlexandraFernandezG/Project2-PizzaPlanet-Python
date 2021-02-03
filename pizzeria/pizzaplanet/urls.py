from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('pedidos', views.pedidos, name="pedidos"),
    path('enviar', views.enviar, name="enviar"),
]