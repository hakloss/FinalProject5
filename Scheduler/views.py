from django.shortcuts import render

# Create your views here.
from django.views import View
from Scheduler.models import *

class CreateAccount(View):
    def get(self, request):
        return render(request, "CreateAccount.html")

    def post(self, request):
        xfname = request.POST.get('fname')
        xlname = request.POST.get('lname')

        account = user(fname=xfname, lname=xlname)
        account.save()

        return render(request, "CreateAccount.html",{"fname": user, "lname": user})

class Home(View):
    def get(self, request):
        return render(request, "Home.html")

    def post(self, request):
        return render(request, "Home.html")

class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        return render(request, "Login.html")

class CreateCourse(View):
    def get(self, request):
        return render(request, "CreateCourse.html")

    def post(self, request):
        return render(request, "CreateCourse.html")