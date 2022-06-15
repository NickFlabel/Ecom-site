import json
import phonenumbers
from django.core.exceptions import ValidationError
from . import models


def cookieCart(request):
    """This function takes a request and checks for a cookie containing JSON with
    all the products added to the cart by the unathenticated user and returns
    dictionary containing all said items

    return: dict
    """
    try:
        cart = json.loads(request.COOKIES['cart'])
        print(cart)
    except KeyError:
        cart = {}

    items =[]
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = models.Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    """This function takes request and checks for an opened order by the
    authenticated user. If such order is preset it queries the contents of
    such order. If user is not authenticated it checks for a cookie with
    the order
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer.user_id.username)
        order, created = models.Order.objects.get_or_create(customer_id=customer, is_paid=False,
        complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}


def guestOrder(request, data):
    """This function takes request and data from the checkout form and
    creates an order with customer set as customer without the user
    """

    # Fetch data from the form
    name = data['form']['name']
    phone_number = data['form']['phone_number']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # Checks if this customer already exists or not
    customer, created = models.Customer.objects.get_or_create(
        phone_number=phone_number
        )

    customer.name = name
    customer.save()

    # Create new order for this customer
    order = models.Order.objects.create(
        customer_id=customer,
        complete=False,
        is_paid=False
        )

    # Add items from cookie cart to the order
    for item in items:
        product = models.Product.objects.get(id=item['product']['id'])
        orderItem = models.OrderItem.objects.create(
            product_id=product,
            order_id=order,
            quantity=item['quantity']
            )

    return customer, order


def add_bonuses_for_transaction(request, customer, sum_of_transaction):
    """This function adds or removes bonuses from the customer
    """
    number_of_bonuses = round(sum_of_transaction * 0.05)
    new_boni = models.Bonuses.objects.create(
        number_of_bonuses = number_of_bonuses,
        customer_id = customer,
        worker_id = request.user,
        )
    return new_boni.number_of_bonuses



def phone_validator(phone_number):
    number = phonenumbers.parse(phone_number, 'RU')
    if not phonenumbers.is_valid_number(number):
        raise ValidationError('This phone number is not valid: ', phone_number)

