from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Cafe(models.Model):
    adress = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.adress


class Customer(models.Model):
    phone_regex = RegexValidator(regex=r'^\+\d{11}$|^8\d{10}$|^\(\d{3}\)\d{7}$|^\(\d{3}\)\d{3}\-\d{2}\-\d{2}$', message='Please, enter the valid phone number')
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField('Phone Number', validators=[phone_regex], max_length=25)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    bonuses = models.IntegerField(default=0)

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

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping


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








