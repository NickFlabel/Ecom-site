from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Customer
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number']


class UserEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']