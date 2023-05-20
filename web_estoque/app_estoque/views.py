import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from app_estoque.models import *
from django.db.models import F, Sum, DateField, TextField
from django.db.models.functions import Trunc, TruncMonth, Cast, Round
from datetime import datetime
from django.contrib.auth import authenticate, login, logout

from django.db.models.deletion import ProtectedError

# Create your views here.

def index(request):
    return HttpResponse("Pagina Inicial")

def teste(request):
    return render(request, 'teste.html')

def template(request):
    return render(request, 'template.html')

def faz_logout(request):
    logout(request)
    return redirect(autenticacao)

def autenticacao(request):
    resposta = {}
    print(request.user)

    if request.POST:
        username = request.POST['user']
        password = request.POST['pswd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
        else:
            resposta['erro'] = "Usuário ou senha inválidos."

    if request.user.is_authenticated:
        return redirect(pagina_compra)


    return render(request, 'autenticacao.html', resposta)

def pagina_compra(request):

    if not request.user.is_authenticated:
        return redirect(autenticacao)

    retorno = {}

    retorno['itens']   = Itens.objects.all()

    if request.POST:

        try:
            deletar = request.POST['deletar']
        except:
            deletar = ''
            print('não foi post de delete')

        if deletar != '':
            try:
                Compra.objects.filter(compra_id=request.POST['deletar']).delete()
            except ProtectedError as e:
                retorno['erro'] = 'Existe Dados dependentes dessa Compra. É necessário apaga-los antes de apagar a compra'
                print(e)
            except:
                print('Outro Erro')


        try:
            id_item = int(request.POST['item'][1:request.POST['item'].index(']')])
            data_compra = request.POST['data_compra']
            numero_referencia = request.POST['n_identificacao']
            fornecedor = request.POST['fornecedor']
            fk_item_id = Itens.objects.get(item_id = id_item)
            quantidade = request.POST['quantidade']
            custo_unitario = request.POST['custo']
            validade = request.POST['validade']
            restantes = request.POST['quantidade']

            valor = request.POST['venda']
        except:
            id_item=False
            print('Não foi Post de inserção')

        if id_item:
            if valor == '':
                valor = Compra.encontrar_ultimo_valor(id_item)
                print(valor)
            if valor:
                c = Compra(
                    data_compra         = data_compra,
                    numero_referencia   = numero_referencia,
                    fornecedor          = fornecedor,
                    fk_item_id          = fk_item_id,
                    quantidade          = quantidade,
                    custo_unitario      = custo_unitario,
                    valor_de_venda      = valor,
                    validade            = validade,
                    restantes           = restantes,
                )
                print(c)
                c.save()
            else:
                retorno['erro'] = 'Não Há registros anteriores desse produto, é necessário atribuir valor'



    retorno['compras'] = Compra.objects.all().order_by('-data_compra')
    return render(request, 'pagina_compra.html', retorno)


def cadastro(request):

    if not request.user.is_authenticated:
        return redirect(autenticacao)


    retorno={}


    if request.POST:
        try:
            Itens.objects.filter(item_id=request.POST['deletar']).delete()
        except:
            print('Passou deletar')
        try:

            categoria=request.POST['Categoria']
            marca=request.POST['Marca']
            produto_e_sabor=request.POST['Produto e Sabor']
            tipo=request.POST['Tipo']
            volume=request.POST['Volume']

            i = Itens( categoria=categoria, marca=marca, produto_sabor=produto_e_sabor, tipo=tipo, volume=volume)
            i.save()
        except:
            print('Passou cadastro')

    retorno['produtos'] = Itens.objects.all()

    return render(request, 'pagina_cadastro.html', retorno)


#Testes
def tabela_ex(request):
    produtos = []
    #recuperar todos os itens da tabela para retornar
    return render(request, 'tabela_ex.html')

def delete_item(request):
    if not request.user.is_authenticated:
        return redirect(autenticacao)

    print(request.POST)
    return tabela_ex(request)

def pagina_venda(request):
    if not request.user.is_authenticated:
        return redirect(autenticacao)

    retorno = {}
    retorno['lista_ids'] = range(8)

    retorno['itens'] = Itens.objects.all()

    print(retorno['itens'])

    if request.POST:

        for i in retorno['lista_ids']:
            if request.POST[f'item_{i}']!='' and request.POST[f'quantidade_{i}']!='0':
                id_find = request.POST[f'item_{i}']
                id_find = int(id_find[1:id_find.index(']')])

                print(Itens.objects.get(item_id=id_find))

                Item_Venda.add_venda(id_find, int(request.POST[f'quantidade_{i}']), int(request.POST[f'desconto_{i}']))

    return render(request, 'venda_do_produto.html', retorno)


# Função da view do Relatório
def relatorio(request):

    if not request.user.is_authenticated:
        return redirect(autenticacao)
    #Inicializa variável que irá conter todos os produtos a serem renderizados na pagina
    produtos = []

    #Adiciona a referência dessa variavel ao dic de retorno assim qualquer coisa mudada nela também será enviada
    retorno = {
        'produtos':produtos,
        'list_categ' : Itens.get_categorias()
    }
    retorno['date_default'] = datetime.now().strftime("%Y-%m-%d")
    #Só executa se o metodo for POST, ou seja, quando entra na pagina é o metodo GET e não executa
    if request.POST:
        #Se quiser saber o que vem no metodo use um print dele
        print(request.POST)
        #Retorna erro se  não tiver valor nos campos de inicio e fim (se tiverem campos não validos)

        #Os campos estão prenchidos corretamentes então á é adicionado ao dicionario de resposta as variáveis escolhidas
        retorno['categoria'] = request.POST['categoria']
        retorno['tipo']      = request.POST['vendas-estoque']

        if request.POST['vendas-estoque'] == "Vendas":
            retorno['periodo']   = request.POST['periodo']
            retorno['inicio']    = request.POST['inicio']
            retorno['fim']       = request.POST['fim']

            if (request.POST['inicio'] == '' or request.POST['fim'] == ''):
                retorno['erro'] = "Preencha Todos os Campos!"

            # Retorna erro se a data inicial for maior que a final
            elif parse_date(request.POST['inicio']) > parse_date(request.POST['fim']):
                retorno['erro'] = "A data inicial deve ser menor ou igual que à final!"

            else:
                #-----------------------------
                #Realizar Querry de vendas no DB

                produtos = Item_Venda.vendas_entre(retorno['inicio'], retorno['fim'])

                if retorno['categoria']!="Todas":
                    produtos = produtos.filter(fk_item_id__categoria=retorno['categoria'])

                # --------------------------DESCONTO APLICADO POR COMPRA, SE FRO POR ITEM MODIFICAR-------------

                produtos = produtos.annotate(lucro =  Round((F('fk_compra_id__valor_de_venda')-F('fk_compra_id__custo_unitario'))*F('quantidade')-F('desconto'),2))
                produtos = produtos.annotate(total =  Round( F('fk_compra_id__valor_de_venda') * F('quantidade') ,2)-F('desconto'))
                retorno['quantidade']   = produtos.aggregate(sum = Round(Sum('quantidade'),2))
                retorno['total'] = produtos.aggregate(sum = Round(Sum('total'),2))
                retorno['lucro'] = produtos.aggregate(sum = Round(Sum('lucro'),2))

                print(retorno['lucro'])

                if retorno['periodo']=="Diário":
                    produtos = produtos.annotate(data = F('data_venda'))
                elif retorno['periodo'] == 'Mensal':
                    produtos = produtos.annotate(data = TruncMonth('data_venda', DateField()))
                elif retorno['periodo'] == 'Semanal':
                    produtos = produtos.annotate(data = Trunc('data_venda','week' , DateField()))


                produtos = produtos.values('fk_item_id__marca', 'fk_item_id__produto_sabor', "fk_item_id__tipo",
                                           "fk_item_id__volume", 'data', 'fk_compra_id__custo_unitario',
                                            'fk_compra_id__valor_de_venda')\
                                    .annotate(desconto=Sum('desconto'), quantidade=Sum('quantidade'), total=Round(Sum('total'),2),
                                            lucro=Sum('lucro')).order_by('fk_item_id','data')

                #------------------------------

                #Atribuição das colunas de vendas e dos produtos
                retorno['columns'] = ['Produto', 'Data Referência', 'Custo Unitario', 'Venda R$', 'Desconto' , 'Quantidade', "Total" ,'Lucro']

                retorno['produtos'] = produtos

        elif request.POST['vendas-estoque']=="Estoque":
            #-----------------------------
            produtos = Compra.objects.all().order_by('-restantes')

            if retorno['categoria']!="Todas":
                produtos = produtos.filter(fk_item_id__categoria=retorno['categoria'])

            produtos = produtos.annotate(valor_estoque=Round(F('custo_unitario') * F('restantes'),2))
            produtos = produtos.annotate(lucro_potencial=Round((F('valor_de_venda') - F('custo_unitario'))* F('restantes'),2))

            retorno['quantidade'] = produtos.aggregate     ( sum  = Round(Sum('restantes'),2))
            retorno['valor_estoque'] = produtos.aggregate  ( sum  = Round(Sum('valor_estoque'),2))
            retorno['lucro_potencial'] = produtos.aggregate( sum  = Round(Sum('lucro_potencial'),2))

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
    if not request.user.is_authenticated:
        return redirect(autenticacao)
    #print(request.GET)

    # Criando a resposta e adicionando informações ao protocolo HTTP para ele baixar o arquivo e não mudar de página
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="relatorio_{request.GET["tipo"]}_{request.GET["inicio"]}.csv"'

    # -----------------------------
    # Realizar Querry de Vendas ou Estoque no DB
    print(f'Querry de {request.GET["tipo"]}')

    valores = []
    if request.GET['tipo']=="Vendas":
        produtos = Item_Venda.vendas_entre(request.GET['inicio'], request.GET['fim'])\
            .annotate(item = F("fk_item_id__produto_sabor")) \
            .annotate(marca=F("fk_item_id__marca"))
        produtos = produtos\
            .annotate(custo_unitario=F('fk_compra_id__custo_unitario'))\
            .annotate(valor_unitario_item=F('fk_compra_id__valor_de_venda'))\
            .annotate(valor_total_venda=(F('fk_compra_id__valor_de_venda') * F('quantidade'))-F('desconto'))\
            .annotate(lucro=(F('fk_compra_id__valor_de_venda') - F('fk_compra_id__custo_unitario')) * F('quantidade'))

    else:
        produtos = Compra.objects.all().order_by('-restantes')\
            .annotate(item = F("fk_item_id__produto_sabor")) \
            .annotate(marca=F("fk_item_id__marca"))
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