from django.shortcuts import render
from . import models

def store(request):
    products = models.Product.objects.all()
    ctx = {'products':products}
    return render(request, 'ecom/store.html', ctx)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer,
        complete=False)
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    ctx = {'items': items, 'order': order}
    return render(request, 'ecom/cart.html', ctx)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer,
        complete=False)
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    ctx = {'items': items, 'order': order}
    return render(request, 'ecom/checkout.html', ctx)