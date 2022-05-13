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

class ShippingAddress(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=1024)
  address = models.CharField(max_length=1024)
  city = models.CharField(max_length=1024)
  zip_code = models.CharField(max_length=12)
  state = models.CharField(max_length=2, choices=STATES)
  country = models.CharField(max_length=1024)

  def get_absolute_url(self):
    return reverse('home')

  def __str__(self):
    return f"Customer: {self.name} created by User: {self.user_id}"