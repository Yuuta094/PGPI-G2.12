from django.shortcuts import render, redirect, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from .forms import NewItemForm,EditItemForm
from .models import Category, Artwork, Order, Order_Detail
import json, random, requests


# Create your views here.

@login_required
def new(request):
    request.session["paypal"]
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

def detail(request,artwork_id):
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    related_obras = Artwork.objects.filter(category=artwork.category).exclude(pk=artwork_id)
    return render(request,'product/detail.html', {
        'artwork':artwork,
        'related_obras':related_obras
    })
    
def search_page(request):
    categories = [choice[1] for choice in Category.choices]
    return render(request,'product/search.html', {
        'categories':categories
    })
    
def search(request):
    categories = [choice[1] for choice in Category.choices]
    q = request.GET.get('q')
    category = request.GET.get('category')
    author = request.GET.get('author')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    obras = Artwork.objects.filter(name__icontains=q, category__icontains=category, author__icontains=author)
    if min_price:
        obras = obras.filter(price__gte=min_price)
    if max_price:
        obras = obras.filter(price__lte=max_price)
    return render(request,'product/search.html', {
        'obras':obras,
        'q':q,
        'categories':categories,
        'category':category,
        'author':author,
        'min_price':min_price,
        'max_price':max_price
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


def simple_checkout(request):
    template_name= "product/buttonsPaypal.html"
    return render(request, template_name)

def paymentComplete(request):
    body= json.loads(request.body)
    sess= request.session.get("data",{"items":[]})
    productos_carro=sess["items"]
    
    #Datos cabecera
    oc=Order()
    oc.customer=body['customer']  #el cliente
    oc.ordernum=random.randint(10000,99999)
    oc.save()
    
    #Datos detalles
    for item in productos_carro:
        od=Order_Detail
        prod= Artwork.objects.get(slug=item) #nombre del producto/s
        od.product= prod
        od.cant=1
        od.order=oc
        od.save()
        
    #Borrar session para empezar de 0
    del  request.session['data']
    
    return redirect('product:sucess')

def sucess(request):
    template_name= "product/sucess.html"
    return render(request, template_name)
    