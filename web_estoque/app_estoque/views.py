import csv
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



















def relatorio(request):
    produtos = []


    retorno = {
        'produtos':produtos
    }
    if request.POST:
        #print(request.POST)
        print(request.POST['inicio'])

        if (request.POST['inicio']=='' or request.POST['fim']==''):
            retorno['erro'] = "Preencha Todos os Campos!"

        else:
            retorno['inicio']    = request.POST['inicio']
            retorno['fim']       = request.POST['fim']
            retorno['categoria'] = request.POST['categoria']
            retorno['periodo']   = request.POST['periodo']
            retorno['tipo']      = request.POST['vendas-estoque']


        if request.POST['vendas-estoque'] == "Vendas":
            #Realizar a querry nos filtros escolhidos

            retorno['columns'] = ['Produto', 'Data Referência', 'Custo Unitario', 'Valor Venda', 'Quantidade', 'Lucro']


            produtos.append({'produto':'Coca Cola Tradicional Garrafa 2L', 'data_ref':'21/12/2022', 'custo_unitario':4.99, "valor_venda":5.99, 'quantidade':20,'lucro':1.00})
            produtos.append({'produto': 'Coca Cola Zero Garrafa 2L', 'data_ref': '21/12/2022', 'custo_unitario': 4.99, "valor_venda": 5.99, 'quantidade': 10, 'lucro': 1.00})


        elif request.POST['vendas-estoque']=="Estoque":
            #Realizar a querry nos filtros escolhidos

            retorno['columns']   = ['Descricção do Produto','Data de Validade','Custo Unitario','Quantidade em estoque','Valor total Estoque']

            produtos.append(
                {'produto': 'Coca Cola Tradicional Garrafa 2L', 'data_validade': '21/12/2023', 'custo_unitario': 4.99,
                  'quantidade': 20, 'valor_estoque': 99.80})
            produtos.append({'produto': 'Coca Cola Zero Garrafa 2L', 'data_validade': '21/12/2023', 'custo_unitario': 4.99,
                 'quantidade': 10, 'valor_estoque': 49.90})

    return render(request, 'relatorio.html', retorno)

def download(request):
    #print(request.GET)
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="relatorio_{request.GET["inicio"]}.csv"'

    #Fazer a Querry deste metodo para retornar os valores corretos
    campos = ['Item','Categoria', 'Data Ref', 'Preço Compra', "Preço Venda","Unidades", "Lucro"]
    valores = [
        ['Coca Cola Tradicional Garrafa 2L', 'Refrigerante','2023-04-01', 5.99,6.99,10,10.00 ],
        ['Coca Cola Zero Garrafa 2L', 'Refrigerante', '2023-04-01', 5.99,6.99,6,6.00]
    ]
    writer = csv.writer(response, csv.excel)
    writer.writerow(campos)
    writer.writerows(valores)

    return response