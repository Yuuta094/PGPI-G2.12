
from django.shortcuts import render, redirect, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from .forms import NewItemForm,EditItemForm
from .models import Artwork

# Create your views here.

@login_required
def new(request):
    if request.method== "POST":
        form= NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item= form.save()
            item.created_by = request.user
            item.save()
            
            return redirect('product:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'product/form.html',{
        'form': form, 
        'title': 'NewItem'})


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
    
    if request.method == "POST":
        form= EditItemForm(request.POST, request.FILES, instance=obra)
        
        if form.is_valid():
            form.save()
            
            return redirect('product:detail', pk=obra.id)
    else:
        form = EditItemForm(instance=obra)
    
    return render(request, 'product/form.html',{
        'form': form, 
        'title': 'Edit Item'})
    


@login_required
def delete(request, pk):
    obra= get_object_or_404(Artwork, pk=pk)
    obra.delete()
    
    return redirect('dashboard:index')