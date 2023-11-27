from django.shortcuts import render, redirect
from product.models import Artwork
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    artworks = Artwork.objects.all()
    return render(request, 'core/index.html', {
        'artworks': artworks
    })

def contact(request):
    return render(request, 'core/contact.html', {
    })
    
def about(request):
    return render(request, 'core/about.html', {
    })
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {
        'form': form
    })
        
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "core/logout.html", {})