from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ShippingAddress
from django.contrib.auth.models import User
import requests
import json
import os

# Create your views here.
def home(request):
  response = requests.get(f"{os.environ['MOVIE_DB_ROOT']}genre/movie/list?api_key={os.environ['MOVIE_DB_KEY']}")
  genres = response.json()['genres']
  image_url = os.environ['MOVIE_DB_IMAGE_URL']
  for genre in genres:
    genre['movies']= requests.get(f"{os.environ['MOVIE_DB_ROOT']}discover/movie?api_key={os.environ['MOVIE_DB_KEY']}&with_genres={genre['id']}").json()['results']
  return render(request, 'home.html', {'genres': genres, 'image_url': image_url })

def userprofile(request, user_id):
  # filter to show just the logged in user's address
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
      # redirect user to orders after they long it
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