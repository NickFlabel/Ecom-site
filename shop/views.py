from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
import json
import datetime
from . forms import CreateUserForm, CreateCustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.generic import DetailView

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
    order, created = models.Order.objects.get_or_create(customer_id=customer, complete=False, is_paid=False)

    orderItem, created = models.OrderItem.objects.get_or_create(order_id=order, product_id=product)

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
        order, created = models.Order.objects.get_or_create(customer_id=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()

    return JsonResponse('Payment complete', safe=False)


def registerPage(request):
    user_form = CreateUserForm()
    customer_form = CreateCustomerForm()

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        customer_form = CreateCustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            User = get_user_model()
            user = User.objects.get(username=username)
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            phone_number = customer_form.cleaned_data['phone_number']
            customer = models.Customer(user_id=user, first_name=first_name,
            last_name=last_name, phone_number=phone_number)
            customer.save()
            messages.success(request, 'Account was created for' + username)
            return redirect('ecom:login')

    ctx = {'user_form':user_form, 'customer_form':customer_form}
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


class ProductDetail(DetailView):

    model = models.Product
    template_name = 'ecom/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)

        cartItems = data['cartItems']

        context['cartItems'] = cartItems
        return context







