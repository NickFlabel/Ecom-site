from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
from .utils import cookieCart, cartData, guestOrder, add_bonuses_for_transaction
from .serializers import OrderSerializer, CustomerBonusesSerializer, CustomerSerializer, UserIdSerializer, AllOrdersSerializer
from django.contrib.auth.forms import UserCreationForm
import json
import datetime
from . forms import CreateUserForm, CreateCustomerForm, UserEmailForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, allowed_users, the_same_user
from rest_framework import status
import phonenumbers

def store(request):
    """This view renders the main page of the e-shop showing all the products in the database
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = models.Product.objects.all()
    ctx = {'products':products, 'cartItems': cartItems, 'shipping':False}
    return render(request, 'ecom/store.html', ctx)

def cart(request):
    """This view renders the cart of the user
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    ctx = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'ecom/cart.html', ctx)

def checkout(request):
    """This view renders the checkout page
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    ctx = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'ecom/checkout.html', ctx)


def updateItem(request):
    """This is POST view that is used to add or delete products from user's cart
    """
    data = json.loads(request.body)
    print('data:', data)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    """This view is POST view and used to process the order info
    """
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

    add_bonuses_for_transaction(request, customer, total)

    return JsonResponse('Payment complete', safe=False)


@unauthenticated_user
def registerPage(request):
    """This view is used to render and get POST info from the user in process of registration
    """
    user_form = CreateUserForm()
    customer_form = CreateCustomerForm()

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        customer_form = CreateCustomerForm(request.POST)
        print(customer_form)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            User = get_user_model()
            user = User.objects.get(username=username)
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            phone_number = customer_form.cleaned_data['phone_number']
            phone_number = phonenumbers.parse(phone_number, 'RU')
            phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            customer = models.Customer(user_id=user, first_name=first_name,
            last_name=last_name, phone_number=phone_number)
            customer.save()
            bonuses = models.Bonuses(customer_id = customer)
            bonuses.save()
            messages.success(request, 'Account was created for' + username)
            return redirect('ecom:login')

    ctx = {'user_form':user_form, 'customer_form':customer_form}
    return render(request, 'ecom/register.html', ctx)


@unauthenticated_user
def loginPage(request):
    """This view is used to render login page and check the entered data
    """

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
    """This view is used to logout the user
    """

    logout(request)

    return redirect('ecom:login')


class ProductDetail(DetailView):
    """This view renders a detail page for the chosen product
    """

    model = models.Product
    template_name = 'ecom/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)

        cartItems = data['cartItems']

        context['cartItems'] = cartItems
        return context


def userPage(request):
    """This view renders the userpage
    """
    user = request.user

    data = cartData(request)

    cartItems = data['cartItems']

    ctx = {'user': user, 'cartItems': cartItems}
    return render(request, 'ecom/account.html', ctx)


@allowed_users(allowed_roles=['worker'])
def management(request):
    """This view renders the management page for the worker of the shop
    """
    user = request.user

    if request.method == 'POST':

        if 'add_bonuses' in request.POST:
            phone_number_add = request.POST.get('phone_number_add')
            customer = models.Customer.objects.get(phone_number=phone_number_add)

            number_of_bonuses = int(request.POST.get('number_of_bonuses_add'))

            number = add_bonuses_for_transaction(request, customer, number_of_bonuses)
            messages.info(request, ('Added '+str(number)+' bonuses'))

        elif 'remove_bonuses' in request.POST:
            phone_number_add = request.POST.get('phone_number_remove')
            customer = models.Customer.objects.get(phone_number=phone_number_add)

        return redirect('ecom:management')

    else:
        orders = models.Order.objects.filter(complete=True)
        data = cartData(request)
        cartItems = data['cartItems']
        ctx = {'user': user, 'cartItems': cartItems, 'orders': orders}
        return render(request, 'ecom/management.html', ctx)



@api_view(['GET'])
def orderDetails(request, pk):
    """This API view allows for fetching the order data from the server
    """

    user = request.user

    order = models.Order.objects.get(id=pk)

    #if user != order.customer_id.user_id or 'worker' not in user.groups.all()[0].name:
    #    return redirect('ecom:userpage')

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(['GET'])
def bonusesHistory(request, pk):
    """This API view allows for fetching the bonuses fata from the server
    """
    customer = User.objects.get(id=pk).customer

    serializer = CustomerBonusesSerializer(customer, many=False)

    return Response(serializer.data)


@api_view(['GET'])
@the_same_user
def customerInfo(request, pk):

    customer = User.objects.get(id=pk).customer

    serializer = CustomerSerializer(customer, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
def update_info(request):

    data = request.body

    data = json.loads(data)

    customer = request.user.customer
    data_customer = {
        'phone_number': data['phone_number'],
        'first_name': data['first_name'],
        'last_name': data['last_name']
        }
    form_to_check = CreateCustomerForm(data_customer)
    if form_to_check.is_valid():
        phone_number = phonenumbers.parse(data['phone_number'], 'RU')
        phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        customer.phone_number = phone_number
        customer.first_name = data['first_name']
        customer.last_name = data['last_name']
        customer.save()

    user = customer.user_id
    data_user = {
        'email': data['email']
        }
    form_to_check_2 = UserEmailForm(data_user)
    if form_to_check_2.is_valid():
        user.email = data['email']
        user.save()

    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def get_current_user(request):
    user = request.user
    serializer = UserIdSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_orders(request):
    orders = models.Order.objects.all()
    serializer = AllOrdersSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_customer_by_phone_number(request, phone_number):

    phone_number = phonenumbers.parse(phone_number, 'RU')
    phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)

    customer = models.Customer.objects.get(phone_number=phone_number)

    if customer:
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)








