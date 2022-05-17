from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ShippingAddress, Order, OrderDetail, Movie
from django.contrib.auth.models import User
import requests
import json
import os
import multiprocessing


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
  movie = requests.get(f"{os.environ['MOVIE_DB_ROOT']}movie/{movie_id}?api_key={os.environ['MOVIE_DB_KEY']}").json()
  credits = requests.get(f"{os.environ['MOVIE_DB_ROOT']}movie/{movie_id}/credits?api_key={os.environ['MOVIE_DB_KEY']}").json()['cast'][:10]
  return render(request, 'movies/detail.html', {'movie': movie, 'credits': credits, 'image_url': image_url })


def cart(request):
  try:
    open_order = Order.objects.get(user=request.user.id, checkout_status=False)
    open_order = open_order.order_detail_list()
  except:
    open_order = ''
  return render(request, 'cart/index.html', { 'open_order': open_order })


def checkout(request):
  current_order = Order.objects.get(user=request.user.id, checkout_status=False)
  addresses = ShippingAddress.objects.filter(user=request.user)
  return render(request, 'cart/checkout.html', { 'addresses': addresses, 'current_order': current_order })


def confirm_order(request, order_id):
  current_order = Order.objects.get(id=order_id)
  current_order.checkout_status = True
  current_order.save()
  return render(request, 'cart/confirm_order.html', { 'current_order': current_order })