from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Artwork, Category

from product.forms import EditItemForm
 



# Create your views here.



@login_required
def index(request):   # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    artworks = Artwork.objects.filter() #faltaría filtarlo por el usuario que lo ha creado
    return render(request, 'dashboard/index.html', {
        'artworks': artworks,
    })
    
