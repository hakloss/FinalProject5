from django.db import models

# Create your models here.
class user(models.Model):
    fname = models.CharField(max_length=30, default='empty')
    lname = models.CharField(max_length=30, default='empty')
    email = models.CharField(max_length=30, default='empty')
    password = models.CharField(max_length=30, default='empty')
    role = models.CharField(max_length=30, default='empty')
    address = models.CharField(max_length=40, default='empty')
    city = models.CharField(max_length=40, default='empty')
    state = models.CharField(max_length=2, default='em')
    zip = models.CharField(max_length=5, default='empty')
    pphone = models.CharField(max_length=5, default='empty')
    wphone = models.CharField(max_length=5, default='empty')