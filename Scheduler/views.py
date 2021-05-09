from django.shortcuts import render, redirect
from django.views import View

from Scheduler import functions
from Scheduler.functions import *
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

        if functions.duplicateUserCheck(xemail):
            return render(request, "CreateAccount.html", {"badmsg": "An account for this email already exists"})
        try:
            account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role=xrole,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone)
            account.save()

            return render(request, "CreateAccount.html", {"successmsg":"Account has been created"})
        except ValueError:
            return render(request, "CreateAccount.html", {"badmsg": "Please enter a valid email"})


class Home(View):
    def get(self, request):
        myuser = request.session["username"]
        return render(request, "Home.html",{"username":myuser})

    def post(self, request):
        myuser = request.session["username"]
        return render(request, "Home.html",{"username":myuser})

class AdminHome(View):
    def get(self, request):
        return render(request, "AdminHome.html")

    def post(self, request):
        return render(request, "AdminHome.html")

class InstructorHome(View):
    def get(self, request):
        return render(request, "InstructorHome.html")

    def post(self, request):
        return render(request, "InstructorHome.html")

class TAHome(View):
    def get(self, request):
        return render(request, "TAHome.html")

    def post(self, request):
        return render(request, "TAHome.html")

class Login(View):
    def get(self, request):
        return render(request, "Login.html",{})

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
            return redirect("/Home")


class CreateCourse(View):
    def get(self, request):
        return render(request, "CreateCourse.html")

    def post(self, request):
        xclassname = request.POST.get('classname')
        if functions.duplicateCourseCheck(xclassname):
            return render(request, "CreateCourse.html", {"badmsg": "This course already exists"})

        xcourse = course(classname=xclassname)
        xcourse.save()
        return render(request, "CreateCourse.html", {"successmsg": "Course has been created"})


class AddSection(View):
    def get(self, request):
        myuser = request.session["username"]
        myaccount = user.objects.get(email=myuser)
        allcourses=(course.objects.values())

        courselist=[]
        for i in allcourses:
            courselist.append(i['classname'])

        return render(request, "AddSection.html",{"username": myuser, "account":myaccount, 'courselist':courselist})

    def post(self, request):
        myuser = request.session["username"]
        myaccount = user.objects.get(email=myuser)
        allcourses = (course.objects.values())

        courselist = []
        for i in allcourses:
            courselist.append(i['classname'])



        xcourse = request.POST.get('course')
        xsectionnum = request.POST.get('number')
        xsectiontime = request.POST.get('time')


        if functions.duplicateSectionCheck(xsectionnum,xsectiontime,xcourse):
            return render(request, "CreateCourse.html", {"badmsg": "This course already exists", "username": myuser, 'courselist':courselist})
        try:
            xcourse = course.objects.get(classname=request.POST.get('classname'))
            xsection = section(time=xsectiontime, number=xsectionnum, course=xcourse)
            xsection.save()
            return render(request, "AddSection.html", {"successmsg": "Section has been added","username": myuser, 'courselist':courselist})
        except:
            return render(request, "AddSection.html", {"badmsg": "Section has not been added", "username": myuser, "account":myaccount, 'courselist':courselist})

class ViewAccounts(View):
    def get(self, request):
        allaccounts = user.objects.all()
        return render(request, "ViewAccounts.html", {'obj':allaccounts})

    def post(self, request):
        return render(request, "ViewAccounts.html")

class AssignInstructor(View):
    def get(self, request):
        return render(request, "AssignInstructor.html")

    def post(self, request):
        return render(request, "AssignInstructor.html")

class AssignTA(View):
    def get(self, request):
        myUser = request.session["username"]
        myaccount = user.objects.get(email = myUser)
        allsections = (section.objects.values())

        sections = []
        for i in allsections:
            sections.append(i["number"])


        return render(request, "AssignTA.html", {"unsername": myUser, "account":myaccount, 'sections':sections})

    def post(self, request):
        myUser = request.session["username"]
        myaccount = user.objects.get(email=myUser)
        allsections = (section.objects.values())

        sections = []
        for i in allsections:
            sections.append(i["number"])

        xTA = request.POST.get('ta')

        if functions.duplicateUserCheck(xTA):
            return render(request, "AssignTA.html", {"badmsg": "TA has already been assingned"})
        try:
            xTA = user.objects.get(classname= request.POST.get('classname'))
            xTA = section(ta=xTA)
            xTA.save()
            return render(request, "AssignTA.html", {"succesmsg": "Successfully assigned a TA", "username": myUser, 'sections':sections})
        except:
            return render(request, "AssignTA.html", {"badmsg": "TA has not been assinged", "username": myUser, 'section':sections})

class ViewAssignments(View):
    def get(self, request):
        return render(request, "ViewAssignments.html")

    def post(self, request):
        return render(request, "ViewAssignments.html")

class EditAccount(View):
    def get(self, request):
        myuser = request.session["username"]
        myaccount=user.objects.get(email=myuser)

        return render(request, "EditAccount.html", {"username": myuser, "account":myaccount})

    def post(self, request):
        myuser = request.session["username"]
        myaccount = user.objects.get(email=myuser)

        myaccount.fname = request.POST.get('fname')
        myaccount.lname = request.POST.get('lname')
        myaccount.email = request.POST.get('email')
        myaccount.password = request.POST.get('password')
        myaccount.address = request.POST.get('address')
        myaccount.city = request.POST.get('city')
        myaccount.state = request.POST.get('state')
        myaccount.zip = request.POST.get('zip')
        myaccount.pphone = request.POST.get('pphone')
        myaccount.wphone = request.POST.get('wphone')

        myaccount.save()

        return render(request, "EditAccount.html", {"username": myuser, "successmsg": "Account has been updated", "account":myaccount})
