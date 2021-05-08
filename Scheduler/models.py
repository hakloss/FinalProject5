from django.db import models

# Create your models here.
class user(models.Model):
    fname = models.CharField(max_length=30, default='empty')
    lname = models.CharField(max_length=30, default='empty')
    email = models.EmailField(max_length=254, default='empty', primary_key=True)
    password = models.CharField(max_length=30, default='empty')
    role = models.CharField(max_length=30, default='empty')
    maxsection=models.IntegerField(default=0, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.CharField(max_length=5, null=True, blank=True)
    pphone = models.CharField(max_length=12, null=True, blank=True)
    wphone = models.CharField(max_length=12, null=True, blank=True)

class course(models.Model):
    classname = models.CharField(max_length=30, default='empty', null=True)
    instructor = models.ForeignKey(user, on_delete=models.CASCADE, blank=False, null=True)


class section(models.Model):
    number = models.CharField(max_length=30, default='empty',null=True, blank=True)
    time = models.CharField(max_length=40, default='empty',null=True, blank=True)
    course = models.ForeignKey(course, on_delete=models.CASCADE, blank=False, null=True)

