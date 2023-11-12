from django.shortcuts import render,get_object_or_404
from .models import Artwork


def detail(request,pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request,'product/detail.html',{'artwork':artwork})
