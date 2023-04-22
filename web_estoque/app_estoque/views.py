import csv
from django.shortcuts import render
from django.http import HttpResponse
from app_estoque.models import *

# Create your views here.

def index(request):
    return HttpResponse("Pagina Inicial")

def teste(request):
    return render(request, 'teste.html')




#Testes
def tabela_ex(request):
    produtos = []
    #recuperar todos os itens da tabela para retornar
    return render(request, 'tabela_ex.html')

def delete_item(request):
    print(request.POST)
    return tabela_ex(request)


















# Função da view do Relatório
def relatorio(request):
    #Inicializa variável que irá conter todos os produtos a serem renderizados na pagina
    produtos = []

    #Adiciona a referência dessa variavel ao dic de retorno assim qualquer coisa mudada nela também será enviada
    retorno = {
        'produtos':produtos
    }
    #Só executa se o metodo for POST, ou seja, quando entra na pagina é o metodo GET e não executa
    if request.POST:
        #Se quiser saber o que vem no metodo use um print dele
        #print(request.POST)

        #Retorna erro se  não tiver valor nos campos de inicio e fim (se tiverem campos não validos)
        if (request.POST['inicio']=='' or request.POST['fim']==''):
            retorno['erro'] = "Preencha Todos os Campos!"

        else:
            #Os campos estão prenchidos corretamentes então á é adicionado ao dicionario de resposta as variáveis escolhidas
            retorno['inicio']    = request.POST['inicio']
            retorno['fim']       = request.POST['fim']
            retorno['categoria'] = request.POST['categoria']
            retorno['periodo']   = request.POST['periodo']
            retorno['tipo']      = request.POST['vendas-estoque']


            if request.POST['vendas-estoque'] == "Vendas":
                #-----------------------------
                #Realizar Querry de vendas no DB
                #------------------------------

                #Atribuição das colunas de vendas e dos produtos
                retorno['columns'] = ['Produto', 'Data Referência', 'Custo Unitario', 'Valor Venda', 'Quantidade', 'Lucro']

                produtos.append({'produto':'Coca Cola Tradicional Garrafa 2L', 'data_ref':'21/12/2022', 'custo_unitario':4.99, "valor_venda":5.99, 'quantidade':20,'lucro':1.00})
                produtos.append({'produto': 'Coca Cola Zero Garrafa 2L', 'data_ref': '21/12/2022', 'custo_unitario': 4.99, "valor_venda": 5.99, 'quantidade': 10, 'lucro': 1.00})


            elif request.POST['vendas-estoque']=="Estoque":
                #-----------------------------
                #Realizar Querry de Estoque no DB
                #------------------------------

                # Atribuição das colunas de estoque e dos produtos
                retorno['columns']   = ['Descricção do Produto','Data de Validade','Custo Unitario','Quantidade em estoque','Valor total Estoque']

                produtos.append(
                    {'produto': 'Coca Cola Tradicional Garrafa 2L', 'data_validade': '21/12/2023', 'custo_unitario': 4.99,
                      'quantidade': 20, 'valor_estoque': 99.80})
                produtos.append({'produto': 'Coca Cola Zero Garrafa 2L', 'data_validade': '21/12/2023', 'custo_unitario': 4.99,
                     'quantidade': 10, 'valor_estoque': 49.90})

    #retornar a renderização dos itens:
    # - request como padrão,
    # - qual o template da pasta templates
    # - o dicionário de retorno que utilizaremos as variáveis no template
    return render(request, 'relatorio.html', retorno)


# Função da view de download dentro do relatorio
def download(request):
    #print(request.GET)

    # Criando a resposta e adicionando informações ao protocolo HTTP para ele baixar o arquivo e não mudar de página
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="relatorio_{request.GET["tipo"]}_{request.GET["inicio"]}.csv"'

    # -----------------------------
    # Realizar Querry de Vendas ou Estoque no DB
    print(f'Querry de {request.GET["tipo"]}')
    # ------------------------------

    campos = ['Item','Categoria', 'Data Ref', 'Preço Compra', "Preço Venda","Unidades", "Lucro"]
    valores = [
        ['Coca Cola Tradicional Garrafa 2L', 'Refrigerante','2023-04-01', 5.99,6.99,10,10.00 ],
        ['Coca Cola Zero Garrafa 2L', 'Refrigerante', '2023-04-01', 5.99,6.99,6,6.00]
    ]

    #Criação do stream CSV na resposta para retorno dele
    writer = csv.writer(response, csv.excel)
    writer.writerow(campos)
    writer.writerows(valores)

    return response