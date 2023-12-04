from django.shortcuts import render, HttpResponse, redirect
from core.models import Customer
from django.shortcuts import render, get_object_or_404
from .forms import PurchaseForm, PurchaseNotLoggedForm
from .models import ShoppingCart, CartItem, Order, Order_Detail, orderStatus, Feedback, STATUS
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
    total = float(calculate_total(cart_items))
    if total == 0:
        messages.error(request, 'No hay productos en el carrito.')
        return redirect('core:index')
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PurchaseForm(request.POST)
            if form.is_valid():
                order = Order()
                order.ordernum = random.randint(10000, 99999)
                order.customer = request.user.email #the future order model should link the customer if possible, not just a string
                order.total_price = total
                order.telephone = form.cleaned_data['telephone']
                order.address = form.cleaned_data['address']
                order.country = form.cleaned_data['country']
                order.city = form.cleaned_data['city']
                order.zip_code = form.cleaned_data['zip_code']
                order_detail = [Order_Detail(product=item.artwork, cant=item.quantity, order=order) for item in cart_items]
                order.save()
                order_detail = Order_Detail.objects.bulk_create(order_detail)
                request.session['shopping_cart'] = {}
                if 'save_data' in request.POST:
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    customer.telephone = form.cleaned_data['telephone']
                    customer.address = form.cleaned_data['address']
                    customer.country = form.cleaned_data['country']
                    customer.city = form.cleaned_data['city']
                    customer.zip_code = form.cleaned_data['zip_code']
                    customer.save()
                # Procesar el pago contrareembolso
                return redirect(reverse('shoppingCart:my-order'))
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
                order_detail = [Order_Detail(product=item.artwork, cant=item.quantity, order=order) for item in cart_items]
                order.save()
                order_detail = Order_Detail.objects.bulk_create(order_detail)
                request.session['shopping_cart'] = {}
                return redirect(reverse('core:index'))
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


def myOrder(request):
    orders = Order.objects.filter(customer=request.user.email)
    orderdetails = Order_Detail.objects.all()
    return render(request, "myOrder.html", locals())


def userOrderTrack(request, order_id):
    order = Order.objects.get(id=order_id)
    orderstatus = orderStatus
    return render(request, "userOrderTrack.html", locals())

def unauthenticatedOrderTrack(request):
    order_id = request.GET.get('order_id')
    order = None
    if order_id is not None:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None
    return render(request, "unauthenticatedOrderTrack.html", {'order': order})

def user_feedback(request, order_id):
    customer = request.user.customer
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, order=order, message=request.POST['feedback'])
        messages.success(request, "La reclamación se ha enviado con éxito")
        
    return render(request, "feedback-form.html", locals())

def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage-feedback.html', locals())

def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage-feedback')

def read_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def change_order_status(request, pid):
    order = Order.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('my-order')

def adminOrders(request):
    if not request.user.is_staff:
        return redirect('core:index')
    orders = Order.objects.all()
    orderdetails = Order_Detail.objects.all()
    return render(request, "adminOrders.html", locals())