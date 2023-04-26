from django.db import models

# Create your models here.

class Itens(models.Model):
    item_id   = models.AutoField(primary_key=True)
    nome      = models.CharField(max_length=30)
    volum_ml  = models.IntegerField()
    categoria = models.CharField(max_length=30)

