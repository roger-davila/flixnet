from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/signup/', views.signup, name='signup'),
  path('shipping_address/create/', views.ShippingAddressCreate.as_view(), name='shipping_address_create'),
]