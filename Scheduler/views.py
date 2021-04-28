from django.shortcuts import render, redirect
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
        xrole = request.POST.get('role')
        xaddress = request.POST.get('address')
        xcity = request.POST.get('city')
        xstate = request.POST.get('state')
        xzip = request.POST.get('zip')
        xpphone = request.POST.get('pphone')
        xwphone = request.POST.get('wphone')
        try:
            account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role=xrole,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone)
            account.save()

            return render(request, "CreateAccount.html", {"successmsg":"Account has been created"})
        except ValueError:
            return render(request, "CreateAccount.html", {"badmsg": "Please enter a valid email"})


class Home(View):
    def get(self, request):
        return render(request, "Home.html")

    def post(self, request):
        return render(request, "Home.html")

class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        badPassword = False
        try:
            myuser = user.objects.get(email=request.POST["username"])
            badPassword = (myuser.password != request.POST['password'])
        except:
            return render(request, "Login.html", {"badmsg": "Please enter a valid username"})
        if badPassword:
            return render(request, "Login.html", {"badmsg": "Please enter a valid password"})
        else:
            request.session["username"] = myuser.email
            return redirect("/")


class CreateCourse(View):
    def get(self, request):
        return render(request, "CreateCourse.html")

    def post(self, request):
        xclassname = request.POST.get('classname')

        try:
            xcourse = course(classname=xclassname)
            xcourse.save()
            return render(request, "CreateCourse.html", {"successmsg": "Course has been created"})
        except:
            return render(request, "CreateCourse.html", {"badmsg": "Please enter a valid course name"})

class AddSection(View):
    def get(self, request):
        return render(request, "AddSection.html")

    def post(self, request):
        xcourse = course.objects.get(classname=request.POST.get('classname'))
        xsectionnum = request.POST.get('section_number')
        print(xsectionnum)
        xsectiontime = request.POST.get('section_time')
        print(xsectiontime)

        try:
            xsection = section(time=xsectiontime, number=xsectionnum, course=xcourse)
            xsection.save()
            return render(request, "AddSection.html", {"successmsg": "section has been added"})
        except:
            return render(request, "AddSection.html", {"badmsg": "section has not been added"})

class ViewAccounts(View):
    def get(self, request):
        allaccounts = user.objects.all()
        return render(request, "ViewAccounts.html", {'obj':allaccounts})

    def post(self, request):
        return render(request, "ViewAccounts.html")