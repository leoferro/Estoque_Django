import datetime

from django.db import models

# Create your models here.

class Itens(models.Model):
    item_id             = models.AutoField(primary_key=True)
    categoria           = models.CharField(max_length=30)
    marca               = models.CharField(max_length=30, default="NA")
    produto_sabor       = models.CharField(max_length=30, default="NA")
    tipo                = models.CharField(max_length=30, default="NA")
    volume              = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.marca.upper()} - {self.produto_sabor} - {self.tipo} {self.volume}"

    @staticmethod
    def get_categorias():
        return set(Itens.objects.values_list('categoria', flat=True))



class Item_Venda(models.Model):
    item_venda_id       = models.AutoField(primary_key=True)
    data_venda          = models.DateField(default=datetime.datetime.now)
    fk_item_id          = models.ForeignKey('Itens', on_delete=models.PROTECT)
    quantidade          = models.PositiveSmallIntegerField()
    desconto            = models.FloatField(default=0)
    fk_compra_id        = models.ForeignKey('Compra', on_delete=models.PROTECT, default=1)
    #precisa pegar ligar em qual compra foi para pegar o valor

    def __str__(self):
        return f"{self.data_venda} - {self.quantidade} {self.fk_item_id.produto_sabor}"

    @staticmethod
    def vendas_entre(data_menor, data_maior):
        '''
        call -> Item_Venda.vendas_entre(data_menor, data_maior)

        :param data_menor: Menor data da consulta
        :param data_maior: Maior data da consulta
        :return: Todas as vendas entre essas datas
        '''
        return Item_Venda.objects.filter(data_venda__lte = data_maior, data_venda__gte = data_menor).order_by('data_venda')

    @staticmethod
    def add_venda(id_item, quantidade, desconto=0, data=''):
        '''
        Preferivel utilizar esse metodo para adicionar venda
            pois ja modifica o estoque automaticamente

        :param id_item: numero do id do item
        :param quantidade: quantodade de itens
        :param desconto: valor a ser descontado
        :param data: qual o dia da venda
        :return: None
        '''
        if data=="":
            data = datetime.datetime.now()
        item = Itens.objects.get(item_id=id_item)

        while quantidade>0:
            compra = Compra.encontrar_em_estoque(id_item).first()
            venda = Item_Venda(data_venda=data, quantidade=quantidade, desconto=desconto, fk_item_id=item, fk_compra_id = compra)
            if compra.restantes >= quantidade:
                compra.restantes -= quantidade
                quantidade = 0
            else:
                venda.quantidade = compra.restantes
                quantidade = quantidade - compra.restantes
                compra.restantes = 0
            venda.save()
            compra.save()



class Compra(models.Model):
    compra_id           = models.AutoField(primary_key=True)
    data_compra         = models.DateField()
    numero_referencia   = models.PositiveBigIntegerField()
    fornecedor          = models.CharField(max_length=30)
    fk_item_id          = models.ForeignKey('Itens', on_delete=models.PROTECT)
    quantidade          = models.PositiveSmallIntegerField()
    custo_unitario      = models.FloatField()
    validade            = models.DateField()
    valor_de_venda      = models.FloatField()
    restantes           = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.data_compra} - {self.numero_referencia} - {self.quantidade} {self.fk_item_id.produto_sabor} resta - {self.restantes}"

    @staticmethod
    def encontrar_em_estoque(id):
        '''
        call -> Compras.encontrar_em_estoque(id)

        :param id: Id do produto
        :return: QuerrySet das compras do produto
                    selecionado que ainda estão
                    no estoque ordenados do
                    mais antigo para o mais novo
        '''
        compras = Compra.objects.filter(fk_item_id_id = id)
        compras = compras.filter(restantes__gt = 0)
        compras = compras.order_by("data_compra")
        return compras

    @staticmethod
    def encontrar_ultimo_valor(id):
        '''
        call -> Compras.encontrar_ultimo_valor(id

        :param id: Id do produto
        :return: Float com o valor mais da compra mais
                    recente do produto
        '''
        compras = Compra.objects.filter(fk_item_id_id=id)
        if len(compras)>0:
            compras = compras.order_by("data_compra").last()
            return compras.valor_de_venda
        else:
            return False