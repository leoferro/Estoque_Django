from django.contrib import admin

# Register your models here.

from django.contrib import admin

from . import models

admin.site.register(models.Itens)
admin.site.register(models.Compra)
admin.site.register(models.Item_Venda)