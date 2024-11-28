from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now

from django.conf import settings

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    instock = models.BooleanField(default=True)
    #file
    picture = models.ImageField(upload_to="product", null=True, blank=True)
    specfile = models.FileField(upload_to="specfile", null=True, blank=True)

class contactList(models.Model):
    topic = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.topic

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100, default='member')
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Action(models.Model):
    contactList = models.ForeignKey(contactList, on_delete=models.CASCADE)
    actionDetail = models.TextField()

    def __str__(self):
        return self.contactList.topic