from django.urls import path

from . import views

app_name = 'ecom'
urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='details'),
    path('account/', views.userPage, name='userpage'),

    path('api/orders/all/', views.get_all_orders, name='getAllOrders'),
    path('api/orders/', views.orderDetails, name='order_details_api'),
    path('api/orders/<int:pk>', views.orderDetails, name='order_details'),
    path('api/bonuses/<int:pk>', views.bonusesHistory, name='bonusesHistory'),
    path('api/customer/<int:pk>', views.customerInfo, name='customerInfo'),
    path('api/customer/update', views.update_info, name='updateCustomer'),
    path('api/getCurrentUser/', views.get_current_user, name='getCurrentUser'),
    path('api/customer/<str:phone_number>', views.get_customer_by_phone_number, name="getCustomerByPhone"),

    path('management/', views.management, name='management')
    ]