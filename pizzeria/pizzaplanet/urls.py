from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')   #En views busca funcion index. Ya tengo ruta para llegarle a index
]