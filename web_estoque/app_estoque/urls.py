from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Estoque App"),
    path("teste", views.teste, name="Teste"),

    path("template", views.template, name="template"),

    path("pagina_de_compra", views.pagina_compra, name="pagina_compra"),

    #testes:
    path("tabela_ex", views.tabela_ex, name="tabela_ex"),
    path('delete_item', views.delete_item, name="delete_item"),

    path("relatorio", views.relatorio, name="Date"),
    path("download", views.download, name="download"),
]