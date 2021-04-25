from django.db import models

# Create your models here.
class user(models.Model):
    fname = models.CharField(max_length=30, default='empty')
    lname = models.CharField(max_length=30, default='empty')