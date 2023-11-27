from django.shortcuts import render, HttpResponse, redirect
from core.models import Customer

from .forms import PurchaseForm, PurchaseNotLoggedForm
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PurchaseForm(request.POST)
            if form.is_valid():
                order = Order()
                order.ordernum = random.randint(10000, 99999)
                order.customer = request.user.email #the future order model should link the customer if possible, not just a string
                order.telephone = form.cleaned_data['telephone']
                order.address = form.cleaned_data['address']
                order.country = form.cleaned_data['country']
                order.city = form.cleaned_data['city']
                order.zip_code = form.cleaned_data['zip_code']
                order.save()
                if 'save_data' in request.POST:
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    customer.telephone = form.cleaned_data['telephone']
                    customer.address = form.cleaned_data['address']
                    customer.country = form.cleaned_data['country']
                    customer.city = form.cleaned_data['city']
                    customer.zip_code = form.cleaned_data['zip_code']
                    customer.save()
                # Procesar el pago contrareembolso
        else:
            if hasattr(request.user, 'customer'):
                customer = request.user.customer
                form = PurchaseForm(initial={'telephone': customer.telephone, 'address': customer.address, 'country': customer.country, 'city': customer.city, 'zip_code': customer.zip_code})
            else:
                form = PurchaseForm()
    else:
        if request.method == 'POST':
            form = PurchaseNotLoggedForm(request.POST)
            if form.is_valid():
                order = Order()
                order.ordernum = random.randint(10000, 99999)
                order.customer = form.cleaned_data['customer'] #email
                order.telephone = form.cleaned_data['telephone']
                order.address = form.cleaned_data['address']
                order.country = form.cleaned_data['country']
                order.city = form.cleaned_data['city']
                order.zip_code = form.cleaned_data['zip_code']
                order.save()
        else:
            form = PurchaseNotLoggedForm()
    return render(request, 'shoppincartdetail.html', {'cart_items': cart_items, 'total': total, 'form': form})

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