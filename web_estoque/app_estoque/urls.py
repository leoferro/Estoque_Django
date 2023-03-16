from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Estoque App"),
    path("procurar_volume", views.procurar_volume, name = "procurar_volume")
]
#path("insere", views.insere, name = "insere")