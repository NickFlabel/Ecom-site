from rest_framework.serializers import ModelSerializer, StringRelatedField, CharField
from .models import *
from django.contrib.auth.models import User


class CustomerOwnBonusesSerializer(ModelSerializer):
    """This serializer allows for fetching info about all bonuses connected with
    the user
    """
    class Meta:
        model = Bonuses
        fields = ['number_of_bonuses', 'date_added']


class CustomerBonusesSerializer(ModelSerializer):
    """This serializer allows for fetching total bonuses and bonuses_set info
    for the user
    """
    bonuses_set = CustomerOwnBonusesSerializer(many=True)
    total_bonuses = CharField(required=False)
    class Meta:
        model = Customer
        fields = ['total_bonuses', 'bonuses_set']


class UserSerializer(ModelSerializer):
    """This serializer allows for fetching username and email data
    """
    class Meta:
        model = User
        fields = ['username', 'email']


class CustomerSerializer(ModelSerializer):
    """This serializer allows for fetching all the data connected to the user including
    bonuses as well as user data
    """
    user_id = UserSerializer()
    total_bonuses = CharField(required=False)
    class Meta:
        model = Customer
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'user_id', 'total_bonuses']


class OrderItemSerializer(ModelSerializer):
    """This serializer allows for fetching all the data concerning the items in the given order
    """
    product_id = StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'product_id']


class OrderSerializer(ModelSerializer):
    """This serializer allows for fetching all the data concerning the given order
    """
    customer_id = CustomerSerializer()
    orderitem_set = OrderItemSerializer(read_only=True, many=True)
    class Meta:
        model = Order
        fields = ['date_ordered', 'id',  'transaction_id', 'orderitem_set', 'customer_id', 'is_paid', 'served', 'complete']


class UserIdSerializer(ModelSerializer):
    """This serializer allows for fetching id of a given user
    """
    class Meta:
        model = User
        fields = ['id']


class AllOrdersSerializer(ModelSerializer):
    """This serializer allows for fething data concerning all placed orders
    """
    class Meta:
        model = Order
        fields = ['id', 'is_paid', 'served', 'complete']


class CustomerOrdersSerializer(ModelSerializer):
    order_set = OrderSerializer(many=True)
    class Meta:
        model = Customer
        fields = ['order_set', 'id']






