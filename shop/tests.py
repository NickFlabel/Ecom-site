from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Customer


# Create your tests here.

User = get_user_model()

class UserAuthTestCase(TestCase):
    """This test case checks the registration process and login process as well
    as the creation of customer along the user
    """

    def setUp(self):
        """The setup registers user by posting valid info
        """
        self.user_password = 'test_123_passworD'
        self.user_name = 'test_name'
        self.user_email = 'test@invalid.com'
        self.first_name = 'mr.test'
        self.last_name = 'testonson'
        self.phone_number = '+79991112233'
        self.registration_url = '/register/'
        data = {
            "username":self.user_name,
            "email":self.user_email,
            "password1":self.user_password,
            "password2":self.user_password,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "phone_number":self.phone_number
            }
        self.response = self.client.post(self.registration_url, data, follow=True)

    def test_registration(self):
        """This test checks if the registration done in the previous test was
        properly performed
        """
        status_code = self.response.status_code
        redirect_path = self.response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, settings.LOGIN_URL)
        self.assertEqual(status_code, 200)
        print('Testing registration...')
        print(status_code, redirect_path)

    def test_invalid_data_registration(self):
        """This test checks if the registration with invalid data fails and
        gives an appropriate message
        """
        user_password = 'test_123_passwoRD'
        user_name = 'test_name_2'
        user_email = 'test2@invalid.com'
        first_name = 'mr.wrong'
        last_name = 'wrongson'
        phone_number = '+7111WmmmmmRONG11'
        data = {
            "username":user_name,
            "email":user_email,
            "password1":user_password,
            "password2":user_password,
            "first_name":first_name,
            "last_name":last_name,
            "phone_number":phone_number
            }
        response = self.client.post(self.registration_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertContains(response, 'Please, enter the valid phone number')

    def test_login(self):
        """This test checks if the user registered in the setup can properly
        login
        """
        login_url = settings.LOGIN_URL
        data = {
            "username": self.user_name,
            "password": self.user_password
            }
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, '/')
        self.assertEqual(status_code, 200)

    def test_is_user_created(self):
        """This test checks if the customer was created alongside the user
        """
        user = User.objects.get(customer__first_name=self.first_name)
        print('The name of the user is: ')
        print('Username:', user.username)
        print('Customer name:', user.customer)
        print('User email:', user.email)
        self.assertEqual(user.email, self.user_email)


class UserAdminTestCase(TestCase):

    def setUp(self):
        self.password = 'aDmIn29_05_1453'
        self.user_name = 'test_admin'
        self.user_email = 'testadmin@invalid.com'
        self.user_admin = User(username=self.user_name, email=self.user_email)
        self.user_admin.is_staff = True
        self.user_admin.is_superuser = True
        self.user_admin.set_password(self.password)
        self.user_admin.save()

    def test_user_exists(self):
        user = User.objects.get(username=self.user_name)
        self.assertEqual(user.email, self.user_email)





