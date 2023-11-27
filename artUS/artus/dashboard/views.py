from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Artwork
from django.contrib import messages
from product.forms import EditItemForm

@login_required
def index(request):
    if request.user.is_superuser:
        artworks = Artwork.objects.all()
    else:
        artworks = Artwork.objects.none()  # No artworks for non-superusers
        if not 'No tienes los permisos.' in [str(message) for message in messages.get_messages(request)]:
            messages.error(request, 'No tienes los permisos.')
    return render(request, 'dashboard/index.html', {
        'artworks': artworks,
    })
