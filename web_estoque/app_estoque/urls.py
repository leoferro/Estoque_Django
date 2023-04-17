from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Estoque App"),
    path("teste", views.teste, name="Teste"),
    path("cadastro", views.cadastro, name="Cadastro"),
    path("date", views.date, name="Date"),
]