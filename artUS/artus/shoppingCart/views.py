from django.shortcuts import render, HttpResponse, redirect
from .models import ShoppingCart, CartItem
from product.models import Artwork
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from decimal import Decimal

def add_shoppingcart_from_product_detail(request, artwork_id):
   shopping_cart = request.session.get('shopping_cart', {})
   artwork = Artwork.objects.get(id=artwork_id)
   if str(artwork_id) in shopping_cart:
       shopping_cart[str(artwork_id)]['quantity'] += 1
       shopping_cart[str(artwork_id)]['accum_value'] = float(shopping_cart[str(artwork_id)]['accum_value']) + float(artwork.price)
   else:
       shopping_cart[str(artwork_id)] = {'accum_value': float(artwork.price), 'quantity': 1}
   request.session['shopping_cart'] = shopping_cart
   return redirect('product:detail', artwork_id=artwork_id)


def add_shoppingcart_from_cart(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    if str(artwork_id) in shopping_cart:
       shopping_cart[str(artwork_id)]['quantity'] += 1
       shopping_cart[str(artwork_id)]['accum_value'] = float(shopping_cart[str(artwork_id)]['accum_value']) + float(artwork.price)
    else:
       shopping_cart[str(artwork_id)] = {'accum_value': float(artwork.price), 'quantity': 1}
    request.session['shopping_cart'] = shopping_cart
    request.session.modified = True
    return redirect('shoppingCart:carrito_detail')


def delete(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    if str(artwork_id) in shopping_cart:
        del shopping_cart[str(artwork_id)]
        request.session['shopping_cart'] = shopping_cart
        request.session.modified = True
    return redirect('shoppingCart:carrito_detail')

def substract(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    if str(artwork_id) in shopping_cart:
        if shopping_cart[str(artwork_id)]['quantity'] > 1:
            shopping_cart[str(artwork_id)]['quantity'] -= 1
            shopping_cart[str(artwork_id)]['accum_value'] -= float(Artwork.objects.get(id=artwork_id).price)
        else:
            del shopping_cart[str(artwork_id)]
        request.session['shopping_cart'] = shopping_cart
        request.session.modified = True
    return redirect('shoppingCart:carrito_detail')
def clean(request):
    shopping_cart = request.session.get('shopping_cart', {})
    CartItem.objects.filter(shopping_cart=shopping_cart).delete()
def calculate_total(cart_items):
    return sum(item.accum_value for item in cart_items)    

def carrito_detail(request):
    shopping_cart = request.session.get('shopping_cart', {})
    cart_items = [CartItem(artwork_id=artwork_id, **data) for artwork_id, data in shopping_cart.items()]
    total = calculate_total(cart_items)
    return render(request, 'shoppincartdetail.html', {'cart_items': cart_items, 'total': total})