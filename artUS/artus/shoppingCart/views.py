from django.shortcuts import render, HttpResponse, redirect
from core.models import Customer

from .forms import PurchaseForm, PurchaseNotLoggedForm
from .models import ShoppingCart, CartItem, Order, Order_Detail, orderStatus
from product.models import Artwork
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json, random

from decimal import Decimal
from django.contrib import messages


def add_shoppingcart_from_product_detail(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    quantity = int(request.POST.get('quantity', 1))  
    if quantity > artwork.quantity:
        messages.error(request, 'La cantidad solicitada excede la cantidad disponible de esta obra.')
        return redirect('product:detail', artwork_id=artwork_id)
    if str(artwork_id) in shopping_cart:
        shopping_cart[str(artwork_id)]['quantity'] += quantity
        shopping_cart[str(artwork_id)]['accum_value'] = float(shopping_cart[str(artwork_id)]['accum_value']) + float(artwork.price) * quantity
        artwork.quantity -= quantity
        artwork.save()
    else:
        shopping_cart[str(artwork_id)] = {'accum_value': float(artwork.price) * quantity, 'quantity': quantity}
        artwork.quantity -= quantity
        artwork.save()
    request.session['shopping_cart'] = shopping_cart
    request.session.modified = True
    return redirect('product:detail', artwork_id=artwork_id)


def add_shoppingcart_from_cart(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    if str(artwork_id) in shopping_cart:
        if artwork.quantity < 1 and shopping_cart[str(artwork_id)]['quantity'] > artwork.quantity:
            messages.error(request, 'La cantidad solicitada excede la cantidad disponible de esta obra.')
            return redirect('shoppingCart:carrito_detail')
        else: 
            shopping_cart[str(artwork_id)]['quantity'] += 1
            shopping_cart[str(artwork_id)]['accum_value'] = float(shopping_cart[str(artwork_id)]['accum_value']) + float(artwork.price)
            artwork.quantity -= 1
            artwork.save()
    else:
        shopping_cart[str(artwork_id)] = {'accum_value': float(artwork.price), 'quantity': 1}
        artwork.quantity -= 1
        artwork.save()
    request.session['shopping_cart'] = shopping_cart
    request.session.modified = True
    return redirect('shoppingCart:carrito_detail')


def delete(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    if str(artwork_id) in shopping_cart:
        quantity = shopping_cart[str(artwork_id)]['quantity']
        del shopping_cart[str(artwork_id)]
        request.session['shopping_cart'] = shopping_cart
        request.session.modified = True
        artwork.quantity += int(quantity)
        artwork.save()     
    return redirect('shoppingCart:carrito_detail')


def substract(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    if str(artwork_id) in shopping_cart:
        if shopping_cart[str(artwork_id)]['quantity'] > 1:
            shopping_cart[str(artwork_id)]['quantity'] -= 1
            shopping_cart[str(artwork_id)]['accum_value'] -= float(Artwork.objects.get(id=artwork_id).price)
            artwork.quantity += 1
            artwork.save()
        else:
            del shopping_cart[str(artwork_id)]
            artwork.quantity += 1
            artwork.save()
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PurchaseForm(request.POST)
            if form.is_valid():
                order = Order()
                order.ordernum = random.randint(10000, 99999)
                order.customer = request.user.email #the future order model should link the customer if possible, not just a string
                order.total_price = float(total)
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


def success(request):
    template_name= "shoppingCart/success.html"
    return render(request, template_name)


def myOrder(request):
    order = Order.objects.filter(customer=request.user)
    return render(request, "myOrder.html", locals())


def userOrderTrack(request, order_id):
    order = Order.objects.get(id=order_id)
    orderstatus = orderStatus
    return render(request, "userOrderTrack.html", locals())
