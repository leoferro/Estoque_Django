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
    retorno = {
    }
    produtos = []
    if request.POST:
        #print(request.POST)

        retorno['inicio'] = request.POST['inicio']
        retorno['fim'] = request.POST['fim']
        retorno['categoria'] = request.POST['categoria']
        retorno['periodo'] = request.POST['periodo']
        retorno['tipo'] = request.POST['vendas-estoque']
        retorno['produtos'] = produtos

        produtos.append({'produto':'coca cola 2L Retornável', 'data_ref':'21/12/2022', 'custo_unitario':4.99, "valor_venda":5.99, 'quantidade':20,'lucro':1.00})
        produtos.append({'produto': 'coca cola zero 2L Retornável', 'data_ref': '21/12/2022', 'custo_unitario': 4.99, "valor_venda": 5.99, 'quantidade': 10, 'lucro': 1.00})

    return render(request, 'date.html', retorno)