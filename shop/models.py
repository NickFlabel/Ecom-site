from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models import Sum
from .utils import phone_validator

class Cafe(models.Model):
    adress = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.adress


class Customer(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    phone_number = models.CharField('Phone Number', validators=[phone_validator], max_length=25)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)

    def total_bonuses(self):
        boni = self.bonuses_set.all()
        sum = boni.aggregate(Sum('number_of_bonuses'))
        return sum['number_of_bonuses__sum']

    def __str__(self):
        return self.phone_number


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='Here be descriptions')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError:
            url = '/images/placeholder.png'
        return url


class Order(models.Model):
    PAYMENT_METHODS = (
        (1, 'Cash'),
        (2, 'Online')
        )
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    served = models.BooleanField(default=False, null=True, blank=False)
    is_paid = models.BooleanField(default=False, null=True, blank=False)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHODS, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    cafe_id = models.ForeignKey(Cafe, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product_id.price * self.quantity
        return total

    def __str__(self):
        return self.product_id.name

class Bonuses(models.Model):
    number_of_bonuses = models.IntegerField(default=0, null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)







