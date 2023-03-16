from django.shortcuts import render
from django.http import HttpResponse
from app_estoque.models import Item

# Create your views here.

def index(request):
    return render(request, "form.html")

def procurar_volume(request):
    resp = {}
    if request.method=="POST":
        vol = request.POST.get('volume')
        try:
            resp = {"Items":Item.objects.filter(volume=vol)}
        except:
            resp = {"Items":"Erro"}
    else:
        print('Entrou na pagina')
    return render(request, "procurar_volume.html", resp)