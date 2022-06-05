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
    path('account/orders/<int:pk>', views.orderDetails, name='order_details'),
    ]