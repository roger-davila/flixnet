from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ShippingAddress, Order, OrderDetail, Movie
from django.contrib.auth.models import User
import requests
import json
import os
import multiprocessing
multiprocessing.set_start_method("fork")


# Super Buff Multiprocessing code by TBD
def home(request):
  response = requests.get(f"{os.environ['MOVIE_DB_ROOT']}genre/movie/list?api_key={os.environ['MOVIE_DB_KEY']}")
  genres = response.json()['genres']
  image_url = os.environ['MOVIE_DB_IMAGE_URL']
  multi_pool = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)
  genres = multi_pool.map(get_movies_from_genre, [genre for genre in genres])
  multi_pool.close()
  return render(request, 'home.html', {'genres': genres, 'image_url': image_url })


def get_movies_from_genre(genre):
   genre['movies']= requests.get(f"{os.environ['MOVIE_DB_ROOT']}discover/movie?api_key={os.environ['MOVIE_DB_KEY']}&with_genres={genre['id']}&language=en-US").json()['results']
   return genre


def userprofile(request, user_id):
  if request.user.id != user_id:
    return HttpResponseForbidden('You cannot view what is not yours')
  addresses = ShippingAddress.objects.filter(user=request.user)
  user = User.objects.get(id=user_id)
  # order = ShippingAddress.objects.filter(user=request.user)
  return render(request, 'users/index.html', {'addresses' : addresses , 'user':user})


class ShippingAddressCreate(LoginRequiredMixin, CreateView):
  model = ShippingAddress
  fields=['name', 'address', 'city', 'zip_code', 'state', 'country']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class ShippingAddressUpdate(LoginRequiredMixin, UpdateView):
  model = ShippingAddress
  fields=['name', 'address', 'city', 'zip_code', 'state', 'country']


class ShippingAddressDelete(LoginRequiredMixin, DeleteView):
  model = ShippingAddress
  
  def get_success_url(self):
      return reverse('userprofile', kwargs={'user_id': self.request.user.pk})


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message }
  return render(request, 'registration/signup.html', context)


def search(request):
  query = request.GET.get('search')
  movies = ''
  image_url = ''
  if query:
    movies = requests.get(f"{os.environ['MOVIE_DB_ROOT']}search/movie?api_key={os.environ['MOVIE_DB_KEY']}&query={query}").json()['results']
    image_url = os.environ['MOVIE_DB_IMAGE_URL']
  return render(request, 'movies/search.html', {'movies': movies, 'image_url': image_url})


def movie_detail(request, movie_id):
  image_url = os.environ['MOVIE_DB_IMAGE_URL']
  movie = requests.get(f"{os.environ['MOVIE_DB_ROOT']}movie/{movie_id}?api_key={os.environ['MOVIE_DB_KEY']}&append_to_response=release_dates").json()
  credits = requests.get(f"{os.environ['MOVIE_DB_ROOT']}movie/{movie_id}/credits?api_key={os.environ['MOVIE_DB_KEY']}").json()['cast'][:10]
  cert = get_certification(movie)
  try:
    if Movie.objects.get(api_id=movie_id):
      pass   
  except:
    Movie.objects.create(api_id=movie['id'], name=movie['original_title'], price=2.99)
  return render(request, 'movies/detail.html', {'movie': movie, 'credits': credits, 'image_url': image_url, 'certification': cert })

def get_certification(movie):
  for m in movie['release_dates']['results']:
    if m['iso_3166_1'] == "US":
      return m['release_dates'][0]['certification']

def cart(request):
  try:
    open_order = Order.objects.get(user=request.user.id, checkout_status=False)
    if open_order:
      order_total = open_order.order_total()
      open_order = open_order.order_detail_list()
  except:
    open_order = ''
  return render(request, 'cart/index.html', { 'open_order': open_order, 'order_total':order_total })


def checkout(request):
  form_data = request.POST.get('shipping_address')
  current_order = Order.objects.get(user=request.user.id, checkout_status=False)
  addresses = ShippingAddress.objects.filter(user=request.user)
  return render(request, 'cart/checkout.html', { 'addresses': addresses, 'current_order': current_order })


def confirm_order(request, order_id):
  current_order = Order.objects.get(id=order_id)
  current_order.checkout_status = True
  current_order.save()
  return render(request, 'cart/confirm_order.html', { 'current_order': current_order })


@login_required
def add_to_cart(request):
  addresses = ShippingAddress.objects.filter(user=request.user)
  if len(addresses) == 0:
    message = 'Please create an address to add movie to cart'
    return render(request, 'users/index.html', {'message': message})
  movie_id = request.POST.get('movie_id')
  selected_movie = Movie.objects.get(api_id=movie_id)
  current_order = ''
  try:
    current_order = Order.objects.get(user=request.user, checkout_status=False)
  except:
    pass
  if current_order:
    try:
      order_to_update = OrderDetail.objects.filter(order=current_order, movie=selected_movie)
      q = order_to_update[0].quantity + 1
      order_to_update.update(quantity=q)
      order_to_update[0].set_order_price()
    except:
      OrderDetail.objects.create(order = current_order, movie = selected_movie, quantity=1, price=2.99)
  else:
    addresses = ShippingAddress.objects.filter(user=request.user)
    print('Reaching Line 143')
    default_address = addresses[0]
    new_order = Order.objects.create(user = request.user, ship_address = default_address)
    OrderDetail.objects.create(order = new_order, movie = selected_movie, quantity=1, price=2.99)
  return redirect('cart')


def user_orders(request, user_id):
  orders = Order.objects.filter(user=user_id)
  return render(request, 'users/order_history.html', {'orders': orders})
