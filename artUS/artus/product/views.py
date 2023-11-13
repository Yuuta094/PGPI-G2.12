from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from product.models import Obra
from .forms import EdititemForm



# Create your views here.

@login_required
def edit(request, pk):
    
    obra= get_object_or_404(Obra, pk=pk, created_by=request.user)

    if request.method== "POST":
        form= EdititemForm(request.POST, request.FILES, instance=obra)
        
        if form.is_valid():
            form.save()
            
            return redirect('product:detail', pk=item.id)
    else:
        form = EdititemForm(instance=obra)
    
    return render(request, 'product/form.html',{
        'form': form, 
        'title': 'Edit Item'})
    


@login_required
def delete(request, pk):
    obra= get_object_or_404(Obra, pk=pk, created_by=request.user)
    obra.delete()
    
    return redirect('dashboard:index')