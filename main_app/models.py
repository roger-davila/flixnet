from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

STATES = (
  ('AL', 'AL'), ('AK', 'AK'),
  ('AR', 'AR'), ('CA', 'CA'),
  ('CO', 'CO'), ('CT', 'CT'),
  ('DE', 'DE'), ('DC', 'DC'),
  ('FL', 'FL'), ('GA', 'GA'),
  ('HI', 'HI'), ('ID', 'ID'),
  ('IL', 'IL'), ('IN', 'IN'),
  ('IA', 'IA'), ('KS', 'KS'),
  ('KY', 'KY'), ('LA', 'LA'),
  ('ME', 'ME'), ('MD', 'MD'),
  ('MA', 'MA'), ('MI', 'MI'),
  ('MN', 'MN'), ('MS', 'MS'),
  ('MO', 'MO'), ('MT', 'MT'),
  ('NE', 'NE'), ('NV', 'NV'),
  ('NH', 'NH'), ('NJ', 'NJ'),
  ('NM', 'NM'), ('NY', 'NY'),
  ('NC', 'NC'), ('ND', 'ND'),
  ('OH', 'OH'), ('OK', 'OK'),
  ('OR', 'OR'), ('PA', 'PA'),
  ('PR', 'PR'), ('RI', 'RI'),
  ('SC', 'SC'), ('SD', 'SD'),
  ('TN', 'TN'), ('TX', 'TX'),
  ('UT', 'UT'), ('VT', 'VT'),
  ('VA', 'VA'), ('VI', 'VI'),
  ('WA', 'WA'), ('WV', 'WV'),
  ('WI', 'WI'), ('WY', 'WY'),
)

class Movie(models.Model):
  name = models.CharField(max_length=1024)
  api_id = models.CharField(max_length=1024)
  price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"Movie API Id: {self.api_id} has movie name : {self.name}"

class ShippingAddress(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=1024)
  address = models.CharField(max_length=1024)
  city = models.CharField(max_length=1024)
  zip_code = models.CharField(max_length=12)
  state = models.CharField(max_length=2, choices=STATES)
  country = models.CharField(max_length=1024)

  def get_absolute_url(self):
    return reverse('userprofile', kwargs={'user_id': self.user_id})

  def __str__(self):
    return f"Customer: {self.name} created by User: {self.user_id}"

class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  ship_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
  order_date = models.DateTimeField(auto_now_add=True)
  checkout_status = models.BooleanField(default=False)

  def __str__(self):
    return f"Order: {self.id} created by User: {self.user_id}"
  
  def order_detail_list(self):
    return self.orderdetail_set.all()

class OrderDetail(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"Order Detail: {self.id} movie: {self.movie.name}"
  