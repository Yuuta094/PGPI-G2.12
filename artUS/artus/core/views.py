from django.shortcuts import render, redirect, get_object_or_404
from product.models import Artwork
from django.contrib.auth.models import User
from .forms import SignupForm, UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/show/")
        else:
            return render(request, "core/login.html", {"error": "Invalid username/password."})
    return render(request, "core/login.html", {})

def index(request):
    artworks = Artwork.objects.all()
    return render(request, 'core/index.html', {'artworks': artworks})

def contact(request):
    return render(request, 'core/contact.html', {})
    
def about(request):
    return render(request, 'core/about.html', {})
    
def termsofuse(request):
    return render(request, 'core/termsofuse.html', {
    })    
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})
        
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "core/logout.html", {})

@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                last_user = User.objects.last()
                new_user_id = last_user.id + 1 if last_user else 1
                form.instance.id = new_user_id
                form.save()
                return redirect('/show/')
            except:
                pass
    else:
        form = UserForm()
    return render(request, 'core/create.html', {'form': form})

@login_required
def show_users(request):
    users = User.objects.all()
    return render(request, 'core/show.html', {'users':users})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('/show/')
    else:
        form = UserForm(instance = user)
    return render(request, 'core/edit.html', {'form': form, 'user':user})

@login_required
def destroy_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect("/show/")
