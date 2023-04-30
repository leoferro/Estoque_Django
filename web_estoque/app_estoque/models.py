from django.db import models

# Create your models here.

class Itens(models.Model):
    item_id             = models.AutoField(primary_key=True)
    nome                = models.CharField(max_length=30)
    categoria           = models.CharField(max_length=30)
    marca               = models.CharField(max_length=30, default="NA")
    produto_sabor       = models.CharField(max_length=30, default="NA")
    tipo                = models.CharField(max_length=30, default="NA")
    volume              = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nome} - {self.marca} - {self.categoria} - {self.produto_sabor} - {self.tipo} {self.volume}"

class Item_Venda(models.Model):
    item_venda_id       = models.AutoField(primary_key=True)
    fk_item_id          = models.ForeignKey('Itens', on_delete=models.PROTECT)
    quantidade          = models.PositiveSmallIntegerField()
    desconto            = models.FloatField()


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
        return f"{self.fk_item_id.nome}"