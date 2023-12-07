from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist
import random, json
from .models import *
from .forms import *

#              #
#---- Core ----#
#              #

def index(request):
    artworks = Artwork.objects.all()[0:5]
    return render(request, 'core/index.html', {'artworks': artworks})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', { 'form': form})
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "core/logout.html", {})

def contact(request):
    return render(request, 'core/contact.html', {})
    
def about(request):
    return render(request, 'core/about.html', {})

def termsofuse(request):
    return render(request, 'core/termsofuse.html', {})   

#                   #
#----- Producto ----#
#                   #

@login_required
def new(request):
    if request.method== "POST":
        form= NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item= form.save()
            item.created_by = request.user
            item.save()
            
            return redirect('proyect:detail', artwork_id=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'product/NewAndEdit.html',{
        'form': form, 
        'title': 'Nueva Obra'})

def detail(request,artwork_id):
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    related_obras = Artwork.objects.filter(category=artwork.category).exclude(pk=artwork_id)
    return render(request,'product/detail.html', {
        'artwork':artwork,
        'related_obras':related_obras
    })

@login_required
def edit(request, artwork_id):
    obra= get_object_or_404(Artwork, id=artwork_id)
    if request.method == "POST":
        form= EditItemForm(request.POST, request.FILES, instance=obra)
        if form.is_valid():
            form.save()
            return redirect('proyect:detail', artwork_id=obra.id)
    else:
        form = EditItemForm(instance=obra)
    return render(request, 'product/NewAndEdit.html',{
        'form': form, 
        'title': 'Editar Obra'})
    

@login_required
def delete_item(request, artwork_id):
    obra= get_object_or_404(Artwork, pk=artwork_id)
    obra.delete()
    return redirect('proyect:index')
    
#                   #
#---- Dashboard ----#
#                   #

@login_required
def dashboard(request):   # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    artworks = Artwork.objects.filter() #faltaría filtarlo por el usuario que lo ha creado
    return render(request, 'product/dashboard.html', {
        'artworks': artworks,
    })
    
#                  #
#---- Busqueda ----#
#                  #

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
    obras = Artwork.objects.filter(name__icontains=q, category__icontains=category, author__icontains=author)
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




#               #
#---- Email ----#
#               #

def enviar_correo(order, order_details):
    ASUNTO = 'artus - Resumen de la compra {}'.format(order.created.strftime('%d/%m/%Y %H:%M'))
    template = get_template('shoppingCart/email-order-success.html')
    content = template.render({'email': order.customer.email, 'address':order.address, 'order': order, 'order_details': order_details, 
                               'products': order_details, 'price':order.total_price })
    REMITENTE = settings.EMAIL_HOST_USER
    DESTINATARIO = [order.customer.email]
    send_mail(
        ASUNTO,
        message="",
        from_email=REMITENTE,
        recipient_list=DESTINATARIO,
        html_message=content,
        fail_silently = False
    )
    
    
def enviar_correo_no_registrado(order, order_details):
    ASUNTO = 'artus - Resumen de la compra {}'.format(order.created.strftime('%d/%m/%Y %H:%M'))
    template = get_template('shoppingCart/email-order-success.html')
    content = template.render({'email': order.customer, 'address':order.address, 'order': order, 'order_details': order_details, 
                               'products': order_details, 'price':order.total_price })
    REMITENTE = settings.EMAIL_HOST_USER
    DESTINATARIO = [order.customer]
    send_mail(
        ASUNTO,
        message="",
        from_email=REMITENTE,
        recipient_list=DESTINATARIO,
        html_message=content,
        fail_silently = False
    )

#                 #
#---- Carrito ----#
#                 #


def add_shoppingcart_from_product_detail(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    quantity = int(request.POST.get('quantity', 1))  
    if quantity > artwork.quantity:
        messages.error(request, 'La cantidad solicitada excede la cantidad disponible de esta obra.')
        return redirect('proyect:detail', artwork_id=artwork_id)
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
    return redirect('proyect:detail', artwork_id=artwork_id)



def add_shoppingcart_from_cart(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    if str(artwork_id) in shopping_cart:
        if artwork.quantity < 1 and shopping_cart[str(artwork_id)]['quantity'] > artwork.quantity:
            messages.error(request, 'La cantidad solicitada excede la cantidad disponible de esta obra.')
            return redirect('proyect:carrito_detail')
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
    return redirect('proyect:carrito_detail')


def delete_cart(request, artwork_id):
    shopping_cart = request.session.get('shopping_cart', {})
    artwork = Artwork.objects.get(id=artwork_id)
    if str(artwork_id) in shopping_cart:
        quantity = shopping_cart[str(artwork_id)]['quantity']
        del shopping_cart[str(artwork_id)]
        request.session['shopping_cart'] = shopping_cart
        request.session.modified = True
        artwork.quantity += int(quantity)
        artwork.save()     
    return redirect('proyect:carrito_detail')


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
    return redirect('proyect:carrito_detail')


def clean(request):
    shopping_cart = request.session.get('shopping_cart', {})
    CartItem.objects.filter(shopping_cart=shopping_cart).delete()


def calculate_total(cart_items):
    return sum(item.accum_value for item in cart_items)    


def carrito_detail(request):
    shopping_cart = request.session.get('shopping_cart', {})
    cart_items = [CartItem(artwork_id=artwork_id, **data) for artwork_id, data in shopping_cart.items()]
    total = float(calculate_total(cart_items))
    shipping_cost = 0
    if total == 0:
        messages.error(request, 'No hay productos en el carrito.')
        return redirect('proyect:index')
    if total < 50:
        shipping_cost = 5
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PurchaseForm(request.POST)
            if form.is_valid():
                order = Order()
                order.ordernum = random.randint(10000, 99999)
                order.customer = request.user.email #the future order model should link the customer if possible, not just a string
                order.total_price = total + shipping_cost
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
                order.customer = request.user
                enviar_correo(order, order_detail)
                return redirect(reverse('proyect:my-order'))
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
                order.total_price = total + shipping_cost
                order.telephone = form.cleaned_data['telephone']
                order.address = form.cleaned_data['address']
                order.country = form.cleaned_data['country']
                order.city = form.cleaned_data['city']
                order.zip_code = form.cleaned_data['zip_code']
                order.total_price = total
                order_detail = [Order_Detail(product=item.artwork, cant=item.quantity, order=order) for item in cart_items]
                order.save()
                order_detail = Order_Detail.objects.bulk_create(order_detail)
                request.session['shopping_cart'] = {}
                enviar_correo_no_registrado(order, order_detail)
                return redirect(reverse('proyect:index'))
        else:
            form = PurchaseNotLoggedForm()
    return render(request, 'shoppingCart/shoppincartdetail.html', {'cart_items': cart_items, 'total': total, 'form': form, 'shipping_cost': shipping_cost})


#               #
#---- Admin ----#
#               #

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
    return render(request, 'admin/create.html', {'form': form})

@login_required
def show_users(request):
    users = User.objects.all()
    return render(request, 'admin/show.html', {'users':users})

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
    return render(request, 'admin/edit.html', {'form': form, 'user':user})

@login_required
def destroy_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect("/show/")

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            return redirect('/edit_profile/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'admin/editProfile.html', {'form': form})


#                  #
#---- Category ----#
#                  #

def allCategories(request):
    artworks = Artwork.objects.all()
    return render(request, 'category/allCategories.html', {
        'artworks': artworks,
    })

def stillLife(request):
    artworks = Artwork.objects.filter(category=Category.STILL_LIFE)
    return render(request, 'category/stillLife.html', {
        'artworks': artworks,
    })

def portrait(request):
    artworks = Artwork.objects.filter(category=Category.PORTRAIT)
    return render(request, 'category/portrait.html', {
        'artworks': artworks,
    })

def landscape(request):
    artworks = Artwork.objects.filter(category=Category.LANDSCAPE)
    return render(request, 'category/landscape.html', {
        'artworks': artworks,
    })
    
def abstract(request):
    artworks = Artwork.objects.filter(category=Category.ABSTRACT)
    return render(request, 'category/abstract.html', {
        'artworks': artworks,
    })

def figurative(request):
    artworks = Artwork.objects.filter(category=Category.FIGURATIVE)
    return render(request, 'category/figurative.html', {
        'artworks': artworks,
    })

def surrealism(request):
    artworks = Artwork.objects.filter(category=Category.SURREALISM)
    return render(request, 'category/surrealism.html', {
        'artworks': artworks,
    })

def other(request):
    artworks = Artwork.objects.filter(category=Category.OTHER)
    return render(request, 'category/other.html', {
        'artworks': artworks,
    })  
    
    
    
#              #
#---- Pago ----#
#              #

def paymentComplete(request):
    body = json.loads(request.body)
    sess = request.session.get("data", {"items": []})
    productos_carro = sess["items"]
    # Datos cabecera
    oc = Order()
    oc.customer = body['customer']  # El cliente
    oc.ordernum = random.randint(10000, 99999)
    oc.save()
    # Datos detalles
    order_details = []
    for item in productos_carro:
        od = Order_Detail()
        prod = Artwork.objects.get(name=item)  # Nombre del producto/s
        od.product = prod
        od.cant = 1
        od.order = oc
        od.save()
        order_details.append(od)
    enviar_correo(oc, order_details) 
    return redirect('/')


#               #
#---- Order ----#
#               #

def myOrder(request):
    orders = Order.objects.filter(customer=request.user.email)
    orderdetails = Order_Detail.objects.all()
    return render(request, "order/myOrder.html", locals())

def userOrderTrack(request, order_id):
    order = Order.objects.get(id=order_id)
    orderstatus = orderStatus
    return render(request, "order/userOrderTrack.html", locals())

@login_required
def edit_state_order(request, order_id):
    obra= get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form= EditOrderStateForm(request.POST, request.FILES, instance=obra)
        if form.is_valid():
            form.save()
            return redirect("proyect:index")
    else:
        form = EditOrderStateForm(instance=obra)
    return render(request, 'product/NewAndEdit.html',{
        'form': form, 
        'title': 'Editar Estado'})

def unauthenticatedOrderTrack(request):
    order_id = request.GET.get('order_id')
    order = None
    if order_id is not None:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None
    return render(request, "order/unauthenticatedOrderTrack.html", {'order': order})


def adminOrders(request):
    if not request.user.is_staff:
        return redirect('core:index')
    orders = Order.objects.all()
    orderdetails = Order_Detail.objects.all()
    return render(request, "order/adminOrders.html", locals())


def delete_orders(request, pid):
    order = Order.objects.get(id=pid)
    order.delete()
    return redirect('/all-orders/')



#                  #
#---- FeedBack ----#
#                  #

def my_feedbacks(request):
    feedback = Feedback.objects.filter(customer=request.user)
    return render(request, "feedBack/my-feedbacks.html", locals())


def user_feedback(request, order_id):
    customer = request.user
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        Feedback.objects.create(customer=request.user, order=order, message=request.POST['feedback'])
    return render(request, "feedBack/feedback-form.html", locals())


def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.all()
    customer = None
    try:
        customer = Customer.objects.get(user=request.user)
    except ObjectDoesNotExist:
        pass
    return render(request, 'feedBack/manage-feedback.html', locals())


def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    return redirect('/manage-feedback/')
