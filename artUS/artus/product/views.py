from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm

# Create your views here.

@login_required
def new(request):
    if request.method== "POST":
        form= NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item= form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('product:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'product/form.html',{
        'form': form, 
        'title': 'NewItem'})
    
