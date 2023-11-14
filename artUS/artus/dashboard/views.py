from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from product.models import Artwork
from django.contrib.auth.models import User
from django.contrib import admin



# Create your views here.



@login_required
def index(request):   # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    
    artworks = Artwork.objects.filter(creadted_by=request.user) #faltaría filtarlo
     
    return render(request, 'dashboard/index.html', {
        'artworks': artworks,
    })
