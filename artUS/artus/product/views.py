from django.shortcuts import render,get_object_or_404
from .models import Category, Obra

def detail(request,pk):
    obra = get_object_or_404(Obra, pk=pk)
    related_obras = Obra.objects.filter(category=obra.category).exclude(pk=pk)
    return render(request,'product/detail.html', {
        'obra':obra,
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
    obras = Obra.objects.filter(name__icontains=q, category__icontains=category, author__icontains=author)
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
