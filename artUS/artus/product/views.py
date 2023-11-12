from django.shortcuts import render,get_object_or_404
from .models import Obra

def detail(request,pk):
    obra = get_object_or_404(Obra, pk=pk)
    related_obras = Obra.objects.filter(category=obra.category).exclude(pk=pk)
    return render(request,'product/detail.html', {
        'obra':obra,
        'related_obras':related_obras
    })
