from django.shortcuts import render
from django.views import View
from Scheduler.models import *
# Create your views here.
class CreateAccount(View):
    def get(self, request):
        return render(request, "CreateAccount.html")

    def post(self, request):
        xfname = request.POST.get('fname')
        xlname = request.POST.get('lname')
        xemail = request.POST.get('email')
        xpassword = request.POST.get('password')
        xrole=request.POST.get('role')
        xaddress = request.POST.get('address')
        xcity = request.POST.get('city')
        xstate=request.POST.get('state')
        xzip = request.POST.get('zip')
        xpphone = request.POST.get('pphone')
        xwphone = request.POST.get('wphone')

        account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role=xrole,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone)
        account.save()

        return render(request, "CreateAccount.html", {"successmsg":"Account has been created"})

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