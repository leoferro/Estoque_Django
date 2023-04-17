from django.shortcuts import render
from django.http import HttpResponse
from app_estoque.models import *

# Create your views here.

def index(request):
    return HttpResponse("Pagina Inicial")

def teste(request):
    return render(request, 'teste.html')

def cadastro(request):
    return render(request, 'cadastro_teste.html')

def date(request):
    return render(request, 'date.html')