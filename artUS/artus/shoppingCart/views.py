from django.shortcuts import render, HttpResponse, redirect
from .models import ShoppingCart, CartItem, Order, Order_Detail
from product.models import Artwork
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json, random

@login_required
def add_shoppingcart_from_product_detail(request, artwork_id):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    artwork = Artwork.objects.get(id=artwork_id)
    try:
        cart_item = CartItem.objects.get(shopping_cart=shopping_cart, artwork=artwork)
        cart_item.quantity += 1
        cart_item.accum_value += artwork.price
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(shopping_cart=shopping_cart, artwork=artwork, accum_value=artwork.price, quantity=1)
    cart_item.save()
    return redirect('product:detail', artwork_id=artwork_id)

@login_required
def add_shoppingcart_from_cart(request, artwork_id):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    artwork = Artwork.objects.get(id=artwork_id)
    try:
        cart_item = CartItem.objects.get(shopping_cart=shopping_cart, artwork=artwork)
        cart_item.quantity += 1
        cart_item.accum_value += artwork.price
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(shopping_cart=shopping_cart, artwork=artwork, accum_value=artwork.price, quantity=1)
    cart_item.save()
    return redirect('shoppingCart:carrito_detail')

@login_required
def delete(request, artwork_id):
    shopping_cart = ShoppingCart.objects.get(user=request.user)
    artwork = Artwork.objects.get(id=artwork_id)
    try:
        cart_item = CartItem.objects.get(shopping_cart=shopping_cart, artwork=artwork)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # No se encontró el CartItem, no se hace nada
    return redirect('shoppingCart:carrito_detail')

@login_required
def substract(request, artwork_id):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    try:
        cart_item = CartItem.objects.get(shopping_cart=shopping_cart, artwork__id=artwork_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.accum_value -= cart_item.artwork.price
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('shoppingCart:carrito_detail')


def clean(request):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    CartItem.objects.filter(shopping_cart=shopping_cart).delete()


def calculate_total(cart_items):
    return sum(item.accum_value for item in cart_items)    


@login_required
def carrito_detail(request):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)
    total = calculate_total(cart_items)
    return render(request, 'shoppincartdetail.html', {'cart_items': cart_items, 'total': total})

def paymentComplete(request):
    body = json.loads(request.body)
    sess = request.session.get("data", {"items": []})
    productos_carro = sess["items"]
    print(sess)
    print(body)
    print(productos_carro)
    
    # Datos cabecera
    oc = Order()
    oc.customer = body['customer']  # El cliente
    oc.ordernum = random.randint(10000, 99999)
    oc.save()
    print(oc.customer)
    
    # Datos detalles
    for item in productos_carro:
        od = Order_Detail()
        prod = Artwork.objects.get(name=item)  # Nombre del producto/s
        od.product = prod
        od.cant = 1
        od.order = oc
        od.save()
        print(prod)
    
    # Borrar sesión para empezar de cero
    # del request.session['data']  # Puede que haya que borrarlo 
    
    return redirect('/')

def sucess(request):
    template_name= "shoppingCart/sucess.html"
    return render(request, template_name)