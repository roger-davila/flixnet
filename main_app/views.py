from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ShippingAddress
from django.contrib.auth.models import User

# Create your views here.
def home(request):
  return render(request, 'home.html')

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