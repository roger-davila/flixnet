from django.urls import path
from . import views
from main_app.forms import UserLoginForm
from django.contrib.auth.views import LoginView

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/signup/', views.signup, name='signup'),
  path('accounts/login/', LoginView.as_view(authentication_form = UserLoginForm), name="login"),
  path('movies/search/', views.search, name='search'),
  path('movies/<int:movie_id>', views.movie_detail, name='movie_detail'),
  path('shipping_address/create/', views.ShippingAddressCreate.as_view(), name='shipping_address_create'),
  path('shipping_address/<int:pk>/delete/', views.ShippingAddressDelete.as_view(), name='shipping_address_delete'),
  path('shipping_address/<int:pk>/update/', views.ShippingAddressUpdate.as_view(), name='shipping_address_update'),
  path('user/<int:user_id>/', views.userprofile, name='userprofile'),
  path('user/<int:user_id>/orders', views.user_orders, name='user_orders'),
  path('cart/', views.cart, name='cart'),
  path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
  path('cart/checkout/', views.checkout, name='checkout'),
  path('cart/confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order')
]