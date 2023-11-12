from django.shortcuts import render

from product.models import Obra

# Create your views here.
def index(request):
    obras = Obra.objects.all()[0:3]

    return render(request, 'core/index.html', {
        'obras': obras
    })

def about(request):
    return render(request, 'core/about.html', {
    })