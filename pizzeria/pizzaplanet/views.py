#from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('¡Hola! Usted está en el índice de Pizza Planet')

# Create your views here.
