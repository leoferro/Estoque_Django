from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.pagina_venda, name="venda_do_produto_inicial"),
    path("teste", views.teste, name="Teste"),

    path("template", views.template, name="template"),

    path("auth", views.autenticacao, name="autenticacao"),
    path("logout", views.faz_logout, name="logout"),

    path("pagina_de_compra", views.pagina_compra, name="pagina_compra"),
    path("venda_do_produto", views.pagina_venda, name="venda_do_produto"),
    #testes:
    path("tabela_ex", views.tabela_ex, name="tabela_ex"),
    path('delete_item', views.delete_item, name="delete_item"),

    path("relatorio", views.relatorio, name="Date"),
    path("download", views.download, name="download"),
    path("cadastro", views.cadastro, name="cadastro"),


]