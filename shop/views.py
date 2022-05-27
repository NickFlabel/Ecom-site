from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
import json
import datetime
from . forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = models.Product.objects.all()
    ctx = {'products':products, 'cartItems': cartItems, 'shipping':False}
    return render(request, 'ecom/store.html', ctx)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    ctx = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'ecom/cart.html', ctx)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    ctx = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'ecom/checkout.html', ctx)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId;', productId)

    customer = request.user.customer
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()


    if order.shipping == True:
        models.ShippingAdress.objects.create(
            customer=customer,
            order=order,
            adress=data['shipping']['adress'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )


    return JsonResponse('Payment complete', safe=False)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)
            return redirect('ecom:login')

    ctx = {'form':form}
    return render(request, 'ecom/register.html', ctx)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ecom:store')
        else:
            messages.info(request, 'Username OR password is incorrect')

    ctx = {}
    return render(request, 'ecom/login.html', ctx)

def logoutUser(request):

    logout(request)

    return redirect('ecom:login')










