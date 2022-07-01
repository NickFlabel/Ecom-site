from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.http import JsonResponse
from .utils import cartData, guestOrder, add_bonuses_for_transaction, phone_formating, update_order_item_quantity, process_placed_order, register_new_user
from .serializers import OrderSerializer, CustomerBonusesSerializer, CustomerSerializer, UserIdSerializer, AllOrdersSerializer, CustomerOrdersSerializer
import json
import datetime
from . forms import CreateUserForm, CreateCustomerForm, UserEmailForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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

    products = models.Product.objects.all()
    ctx = {
        'products':products,
        'cartItems': cartItems
        }
    return render(request, 'ecom/store.html', ctx)

def cart(request):
    """This view renders the cart of the user
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    ctx = {
        'items': items,
        'order': order,
        'cartItems': cartItems
        }
    print(ctx)
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

    update_order_item_quantity(productId, action, request)

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    """This view is POST view and used to process the order info
    """
    data = json.loads(request.body)

    process_placed_order(request, data)

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
        if user_form.is_valid() and customer_form.is_valid():
            register_new_user(request, user_form, customer_form)
            messages.success(request, 'Account was created')
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
    if not request.user.is_authenticated:
        return redirect('ecom:store')

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

    order = models.Order.objects.get(id=pk)

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
    """This API view transfers the info on the requested customer
    """

    customer = User.objects.get(id=pk).customer

    serializer = CustomerSerializer(customer, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
def update_info(request):
    """This API view updates the info on the user according to the data in
    the request
    """

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
        phone_number = phone_formating(data['phone_number'])
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
    """This API view transfers the ID of the current user
    """
    user = request.user
    serializer = UserIdSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_orders(request):
    """This API view transfers data containing all placed orders
    """
    orders = models.Order.objects.all()
    serializer = AllOrdersSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_customer_by_phone_number(request, phone_number):
    """This API view transfers data on the user with the corresponding phone number
    """
    try:
        phone_number = phone_formating(phone_number)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    customer = models.Customer.objects.get(phone_number=phone_number)

    if customer:
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@allowed_users(allowed_roles=['worker'])
@api_view(['POST'])
def post_new_bonuses(request):
    data = request.body
    data = json.loads(data)

    worker_id = request.user
    customer_id = models.Customer.objects.get(id=data['customerId'])
    number_of_bonuses = data['numberOfBonuses']

    new_bonus = models.Bonuses(number_of_bonuses=number_of_bonuses, customer_id=customer_id, worker_id=worker_id)
    new_bonus.save()

    return Response(status=status.HTTP_202_ACCEPTED)


@allowed_users(allowed_roles=['worker'])
@api_view(['PUT'])
def order_accept_payment(request):
    data = request.body
    data = json.loads(data)

    order = models.Order.objects.get(id=data['id'])
    order.is_paid = True
    order.save()

    return Response(status=status.HTTP_202_ACCEPTED)


@allowed_users(allowed_roles=['worker'])
@api_view(['PUT'])
def order_serve(request):
    data = request.body
    data = json.loads(data)

    order = models.Order.objects.get(id=data['id'])
    order.served = True
    order.save()

    return Response(status=status.HTTP_202_ACCEPTED)


@allowed_users(allowed_roles=['worker'])
@api_view(['GET'])
def get_customer_orders_by_phone_number(request, phone_number):
    try:
        phone_number = phone_formating(phone_number)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    customer = get_object_or_404(models.Customer, phone_number=phone_number)

    serializer = CustomerOrdersSerializer(customer, many=False)
    return Response(serializer.data)












