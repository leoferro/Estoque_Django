import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from app_estoque.models import *
from django.db.models import F, Sum
from datetime import datetime

# Create your views here.

def index(request):
    return HttpResponse("Pagina Inicial")

def teste(request):
    return render(request, 'teste.html')

def template(request):
    return render(request, 'template.html')

def pagina_compra(request):
    return render(request, 'pagina_compra.html')


#Testes
def tabela_ex(request):
    produtos = []
    #recuperar todos os itens da tabela para retornar
    return render(request, 'tabela_ex.html')

def delete_item(request):
    print(request.POST)
    return tabela_ex(request)

def pagina_venda(request):
    return render(request, 'venda_do_produto.html')


















# Função da view do Relatório
def relatorio(request):
    #Inicializa variável que irá conter todos os produtos a serem renderizados na pagina
    produtos = []

    #Adiciona a referência dessa variavel ao dic de retorno assim qualquer coisa mudada nela também será enviada
    retorno = {
        'produtos':produtos
    }
    retorno['date_default'] = datetime.now().strftime("%Y-%m-%d")
    #Só executa se o metodo for POST, ou seja, quando entra na pagina é o metodo GET e não executa
    if request.POST:
        #Se quiser saber o que vem no metodo use um print dele
        #print(request.POST)

        #Retorna erro se  não tiver valor nos campos de inicio e fim (se tiverem campos não validos)
        if (request.POST['inicio']=='' or request.POST['fim']==''):
            retorno['erro'] = "Preencha Todos os Campos!"

        #Retorna erro se a data inicial for maior que a final
        elif parse_date(request.POST['inicio']) > parse_date(request.POST['fim']):
            retorno['erro'] = "A data inicial deve ser menor ou igual que à final!"

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
                produtos = Item_Venda.vendas_entre(retorno['inicio'], retorno['fim'])
                # --------------------------DESCONTO APLICADO POR COMPRA, SE FRO POR ITEM MODIFICAR-------------
                produtos = produtos.annotate(lucro =  (F('fk_compra_id__valor_de_venda')-F('fk_compra_id__custo_unitario'))*F('quantidade')-F('desconto'))
                produtos = produtos.annotate(total =  F('fk_compra_id__valor_de_venda')*F('quantidade')-F('desconto'))
                retorno['quantidade']   = produtos.aggregate(Sum('quantidade'))
                retorno['total'] = produtos.aggregate(Sum('total'))
                retorno['lucro'] = produtos.aggregate(Sum('lucro'))
                #------------------------------

                #Atribuição das colunas de vendas e dos produtos
                retorno['columns'] = ['Produto', 'Data Referência', 'Custo Unitario', 'Venda R$', 'Desconto' , 'Quantidade', "Total" ,'Lucro']

                retorno['produtos'] = produtos

            elif request.POST['vendas-estoque']=="Estoque":
                #-----------------------------
                produtos = Compra.objects.all().order_by('-restantes')
                produtos = produtos.annotate(valor_estoque=F('custo_unitario') * F('restantes'))
                produtos = produtos.annotate(lucro_potencial=(F('valor_de_venda') - F('custo_unitario'))* F('restantes'))

                retorno['quantidade'] = produtos.aggregate(Sum('restantes'))
                retorno['valor_estoque'] = produtos.aggregate(Sum('valor_estoque'))
                retorno['lucro_potencial'] = produtos.aggregate(Sum('lucro_potencial'))

                #------------------------------
                # Atribuição das colunas de estoque e dos produtos
                retorno['columns'] = ['Descricção do Produto','Referencia','Data da Compra', 'Validade',"Custo Unidade R$", 'Venda R$', 'Unidades Estoque', 'Valor Parado', "Lucro Potencial"]
                retorno['produtos'] = produtos


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

    valores = []
    if request.GET['tipo']=="Vendas":
        produtos = Item_Venda.vendas_entre(request.GET['inicio'], request.GET['fim'])
        produtos = produtos\
            .annotate(lucro=(F('fk_compra_id__valor_de_venda') - F('fk_compra_id__custo_unitario')) * F('quantidade'))
    else:
        produtos = Compra.objects.all().order_by('-restantes')
        produtos = produtos.annotate(valor_estoque=F('custo_unitario') * F('restantes'))
        produtos = produtos.annotate(lucro_potencial=(F('valor_de_venda')-F('custo_unitario')) * F('restantes'))
        # ------------------------------

        # Atribuição das colunas de estoque e dos produtos
    # ------------------------------

    campos = list(produtos.values()[0].keys())
    valores = list(produtos.values_list())

    #Criação do stream CSV na resposta para retorno dele
    writer = csv.writer(response, csv.excel)
    writer.writerow(campos)
    writer.writerows(valores)

    return response