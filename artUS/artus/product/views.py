from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from .models import Artwork
from .forms import EdititemForm

# Create your views here.

def detail(request,pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    related_obras = Artwork.objects.filter(category=artwork.category).exclude(pk=pk)
    return render(request,'product/detail.html', {
        'artwork':artwork,
        'related_obras':related_obras
    })


@login_required
def edit(request, pk):
    
    obra= get_object_or_404(Artwork, pk=pk)

    if request.method== "POST":
        form= EdititemForm(request.POST, request.FILES, instance=obra)
        
        if form.is_valid():
            form.save()
            
            return redirect('product:detail', pk=obra.id)
    else:
        form = EdititemForm(instance=obra)
    
    return render(request, 'product/form.html',{
        'form': form, 
        'title': 'Edit Item'})
    


@login_required
def delete(request, pk):
    obra= get_object_or_404(Artwork, pk=pk)
    obra.delete()
    
    return redirect('dashboard:index')