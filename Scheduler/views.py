from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from Scheduler import functions
from Scheduler.functions import *
from Scheduler.models import *

# Create your views here.
class CreateAccount(View):
    def get(self, request):

        return render(request, "CreateAccount.html")

    def post(self, request):
        xrole = request.POST.get('role')
        print(request)
        request.session['role'] = xrole
        if xrole=="TA":
            return redirect("/CreateTA")
        else:
            return redirect("/CreateOther",{'role':xrole})

class CreateTA(View):
    def get(self, request):
        return render(request, "CreateTA.html")

    def post(self, request):
        xfname = request.POST.get('fname')
        xlname = request.POST.get('lname')
        xemail = request.POST.get('email')
        xpassword = request.POST.get('password')
        xmaxsection=request.POST.get('maxsection')
        xskills=request.POST.get('skills')
        xaddress = request.POST.get('address')
        xcity = request.POST.get('city')
        xstate = request.POST.get('state')
        xzip = request.POST.get('zip')
        xpphone = request.POST.get('pphone')
        xwphone = request.POST.get('wphone')

        if not functions.validateEmail(xemail):
            return render(request, "CreateTA.html", {"badmsg": "Please enter a valid email"})
        if functions.duplicateUserCheck(xemail):
            return render(request, "CreateTA.html", {"badmsg": "An account for this email already exists"})

        account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role="TA", maxsection=xmaxsection, skills=xskills,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone)
        account.save()

        return render(request, "CreateTA.html", {"successmsg":"Account has been created"})


class CreateOther(View):
    def get(self, request):
        role=request.session['role']
        return render(request, "CreateOther.html")

    def post(self, request):
        xfname = request.POST.get('fname')
        xlname = request.POST.get('lname')
        xemail = request.POST.get('email')
        xpassword = request.POST.get('password')
        xaddress = request.POST.get('address')
        xcity = request.POST.get('city')
        xstate = request.POST.get('state')
        xzip = request.POST.get('zip')
        xpphone = request.POST.get('pphone')
        xwphone = request.POST.get('wphone')

        xrole = request.session['role']

        if not functions.validateEmail(xemail):
            return render(request, "CreateOther.html", {"badmsg": "Please enter a valid email"})
        if functions.duplicateUserCheck(xemail):
            return render(request, "CreateOther.html", {"badmsg": "An account for this email already exists"})

        account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role=xrole,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone)
        account.save()
        return render(request, "CreateOther.html", {"successmsg":"Account has been created"})



class Home(View):
    def get(self, request):
        #myuser = request.session["username"]
        acc=getAccount(request)
        if acc.role == "admin" or acc.role == "Admin":
            return redirect("/AdminHome")
        elif acc.role == "Instructor" or acc.role == "instructor":
            return redirect("/InstructorHome")
        else:
            return redirect("/TAHome")
        return render(request, "Home.html",{"account":acc, "username":myuser})

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
            return render(request, "Login.html", {"badmsg": "Please enter valid login credentials"})
        if badPassword:
            return render(request, "Login.html", {"badmsg": "Please enter valid login credentials"})
        else:
            request.session["username"] = myuser.email
            return redirect("/Home", {"username": myuser})


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
        acc = functions.getAccount(request)
        return render(request, "ViewAccounts.html", {'obj':allaccounts, 'account':acc})

    def post(self, request):

        #delemail2=get_object_or_404(user, pk=delemail)
        #a = user.objects.get(email=myuser)
        #a.delete()
        #delemail=request.POST.get('delemail')
        #allaccounts = user.objects.all()
        #acc = functions.getAccount(request)
        return render(request, "ViewAccounts.html",{})

class AssignInstructor(View):
    def get(self, request):
        return render(request, "AssignInstructor.html")

    def post(self, request):
        return render(request, "AssignInstructor.html")

class AssignTA(View):
    def get(self, request):
        myUser = request.session["username"]
        myaccount = user.objects.get(email = myUser)

        return render(request, "AssignTA.html", {"username": myUser, "account":myaccount, "courselist":courseList(), "sectionlist":sectionList(), "talist":TAlist()})

    def post(self, request):
        myUser = request.session["username"]
        myaccount= user.objects.get(email=myUser)

        xcourse = request.POST.get('course')
        xsectionnum = request.POST.get('section')
        xta = request.POST.get('ta')

        print(xsectionnum)

        mysection = section.objects.get(number=xsectionnum)
        mysection.ta=xta
        mysection.save()
        return render(request, "AssignTA.html", {"succesmsg": "Successfully assigned a TA", "username": myUser, "courselist":courseList(), "sectionlist":sectionList(), "talist":TAlist()})


class ViewAssignments(View):
    def get(self, request):
        return render(request, "ViewAssignments.html",{})

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

class Denied(View):
    def get(self, request):
        return render(request, "denied.html")
    def post(self, request):
        return render(request, "denied.html")
