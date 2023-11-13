from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

from product.models import Obra

@login_required
def index(request):
    obra = Obra.objects.filter(create_by=request.user)
    
    
    return render(request, 'dashboard/index.html',{
        'obras': obra,
    })