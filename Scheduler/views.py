from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from Scheduler import functions
from Scheduler.functions import *
from Scheduler.models import *

# Create your views here.
class CreateAccount(View):
    def get(self, request):
        if not checkAdminRole(request.session["username"]):
            return redirect("/Denied")
        return render(request, "CreateAccount.html", {"username": myuser(request)})

    def post(self, request):
        xrole = request.POST.get('role')
        request.session['role'] = xrole
        if xrole=="TA":
            return redirect("/CreateTA", {"username": myuser(request)})
        else:
            return redirect("/CreateOther",{'role':xrole, "username": myuser(request)})

class CreateTA(View):
    def get(self, request):
        if not checkAdminRole(request.session["username"]):
            return redirect("/Denied")
        return render(request, "CreateTA.html", {"username": myuser(request)})

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
        xremainingSection=request.POST.get('maxsection')

        if not functions.validateEmail(xemail):
            return render(request, "CreateTA.html", {"badmsg": "Please enter a valid email", "username": myuser(request)})
        if functions.duplicateUserCheck(xemail):
            return render(request, "CreateTA.html", {"badmsg": "An account for this email already exists", "username": myuser(request)})

        account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role="TA", maxsection=xmaxsection, skills=xskills,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone, remainingSection=xremainingSection)
        account.save()

        return render(request, "CreateTA.html", {"successmsg":"Account has been created","username": myuser(request)})


class CreateOther(View):
    def get(self, request):
        if not checkAdminRole(request.session["username"]):
            return redirect("/Denied")
        role=request.session['role']
        return render(request, "CreateOther.html", {"username": myuser(request)})

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
            return render(request, "CreateOther.html", {"badmsg": "Please enter a valid email","username": myuser(request)})
        if functions.duplicateUserCheck(xemail):
            return render(request, "CreateOther.html", {"badmsg": "An account for this email already exists","username": myuser(request)})

        account = user(fname=xfname, lname=xlname, email=xemail, password=xpassword, role=xrole,
                       address=xaddress, city=xcity, state=xstate, zip=xzip, pphone=xpphone, wphone=xwphone)
        account.save()
        return render(request, "CreateOther.html", {"successmsg":"Account has been created", "username": myuser(request)})



class Home(View):
    def get(self, request):

        acc=getAccount(request)
        if acc.role == "admin" or acc.role == "Admin":
            return redirect("/AdminHome",{"username": myuser(request)})
        elif acc.role == "Instructor" or acc.role == "instructor":
            return redirect("/InstructorHome",{"username": myuser(request)})
        else:
            return redirect("/TAHome",{"username": myuser(request)})

    def post (self, request):
        return redirect("/TAHome", {"username": myuser(request)})

class AdminHome(View):
    def get(self, request):
        if not checkAdminRole(myuser(request)):
            return redirect("/Denied")
        return render(request, "AdminHome.html", {"username": myuser(request)})

    def post(self, request):
        return render(request, "AdminHome.html", {"username": myuser(request)})

class InstructorHome(View):
    def get(self, request):
        if not checkInstructorRole(myuser(request)):
            return redirect("/Denied")
        return render(request, "InstructorHome.html",{"username": myuser(request)})
    def post(self, request):
        return render(request, "InstructorHome.html", {"username": myuser(request)})

class TAHome(View):
    def get(self, request):
        if not checkTARole(myuser(request)):
            return redirect("/Denied")
        return render(request, "TAHome.html",{"username": myuser(request)})
    def post(self, request):
        return render(request, "TAHome.html", {"username": myuser(request)})

class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        try:
            myuser = user.objects.get(email=request.POST["username"])
            badPassword = (myuser.password != request.POST['password'])
        except:
            return render(request, "Login.html", {"badmsg": "Please enter valid login credentials"})
        if badPassword:
            return render(request, "Login.html", {"badmsg": "Please enter valid login credentials"})
        else:
            request.session["username"] = myuser.email
            return redirect("/Home",{"username":myuser})


class CreateCourse(View):
    def get(self, request):
        if not checkAdminRole(myuser(request)):
            return redirect("/Denied")
        return render(request, "CreateCourse.html",{"username": myuser(request)})

    def post(self, request):
        xclassname = request.POST.get('classname')
        if functions.duplicateCourseCheck(xclassname):
            return render(request, "CreateCourse.html", {"badmsg": "This course already exists", "username": myuser(request)})

        xcourse = course(classname=xclassname)
        xcourse.save()
        return render(request, "CreateCourse.html", {"successmsg": "Course has been created", "username": myuser(request)})


class AddSection(View):
    def get(self, request):
        if not checkAdminRole(myuser(request)):
            return redirect("/Denied")

        return render(request, "AddSection.html",{'courselist':courseList(), "username": myuser(request)})

    def post(self, request):
        myaccount = user.objects.get(email=myuser(request))
        allcourses = (course.objects.values())

        xcourse = request.POST.get('course')
        xsectionnum = request.POST.get('number')
        xsectiontime = request.POST.get('time')

        if functions.duplicateSectionCheck(xsectionnum,xsectiontime,xcourse):
            return render(request, "CreateCourse.html", {"badmsg": "This course already exists", "username": myuser(request), 'courselist':courseList()})
        try:
            xcourse = course.objects.get(classname=request.POST.get('classname'))
            xsection = section(time=xsectiontime, number=xsectionnum, course=xcourse)
            xsection.save()
            return render(request, "AddSection.html", {"successmsg": "Section has been added","username": myuser(request), 'courselist':courseList()})
        except:
            return render(request, "AddSection.html", {"badmsg": "Section has not been added", "username": myuser(request), "account":myaccount, 'courselist':courseList()})

class ViewAccounts(View):
    def get(self, request, **kwargs):
        if checkAdminRole(myuser(request)) == True or checkInstructorRole(myuser(request)) == True or checkTARole(
                myuser(request)) == True:
            if not request.session.get("username"):
                return redirect("home")

            myacc=user.objects.get(email=myuser(request))
            allaccounts = user.objects.all()

            try:
                deluser = self.kwargs["username"]
            except KeyError:
                return render(request, "ViewAccounts.html", {"badmsg": "Account has not been deleted", 'obj': allaccounts,"username": myuser(request), "account":myacc})

            user.objects.filter(email=deluser).delete()

            return render(request, "ViewAccounts.html", {"successmsg": "Account has been deleted", 'obj': allaccounts,"username": myuser(request), "account":myacc})
        else:
            return redirect("/Denied")


    def post(self, request):
        myacc = user.objects.get(myuser(request))
        delname = request.POST['name']
        print(delname)

        if delname == '':
            allaccounts = user.objects.all()
            return render(request, "ViewAccounts.html", {'name': allaccounts, "account":myacc, "username": myuser(request)})

        allaccounts = user.objects.filter(delname_first=delname)
        print(allaccounts)
        return render(request, "ViewAccounts.html", {'name': allaccounts, "account":myacc, "username": myuser(request)})

class AssignInstructor(View):
    def get(self, request):

        if not checkAdminRole(myuser(request)):
            return redirect("/Denied")
        return render(request, "AssignInstructor.html", {'courselist':courseList(), 'allinstructors': instructorList()})

    def post(self, request):

        if not checkAdminRole(myuser(request)):
            return redirect("/Denied")

        try:
            classname = request.POST.get('classname')
            coursename = course.objects.get(classname=classname)
            lastname = getLastName(request.POST.get('instructor'))
            instructor = user.objects.get(lname=lastname)

            coursename.instructor = instructor
            coursename.save()

            return render(request, "AssignInstructor.html", {'courselist':courseList(), 'allinstructors': instructorList(),
                                                             'successmsg': "Instructor was assigned to course"})

        except:
            return render(request, "AssignInstructor.html", {'courselist':courseList(), 'allinstructors': instructorList(),
                                                             'badmsg': "Instructor was not assigned to course"})

class SelectCourse(View):
    def get(self, request):
        if not checkInstructorRole(myuser(request)):
            return redirect("/Denied")

        return render(request, "SelectCourse.html",{"username": myuser(request), "courselist":courseList()})

    def post(self, request):
        if not checkInstructorRole(myuser(request)):
            return redirect("/Denied")

        xcourse = request.POST.get('classname')
        request.session['course'] = xcourse

        return redirect("/AssignTA", {"course": xcourse, "username": myuser(request)})


class AssignTA(View):
    def get(self, request):
        if not checkInstructorRole(myuser(request)):
            return redirect("/Denied")
        xcourse = request.session['course']

        return render(request, "AssignTA.html", {"username": myuser(request), "sectionlist":sectionList(xcourse), "talist":TAlist()})

    def post(self, request):
        if not checkInstructorRole(myuser(request)):
            return redirect("/Denied")

        xcourse = request.session['course']
        xsectionnum = request.POST.get('section')
        xta = request.POST.get('ta')

        mysection = section.objects.get(number=xsectionnum)
        mysection.ta=user.objects.get(email=xta)
        mysection.save()

        functions.maxSectionTally(xta)

        if user.objects.get(email=xta).remainingSection==0:
            return render(request, "AssignTA.html", {"badmsg": "TA has no available sections", "username": myuser(request), "sectionlist":sectionList(xcourse), "talist":TAlist()})
        return render(request, "AssignTA.html", {"successmsg": "Successfully assigned a TA", "username": myuser(request),
                                                 "sectionlist": sectionList(xcourse), "talist": TAlist()})


class ViewAssignments(View):
    def get(self, request):
        if checkAdminRole(myuser(request))==True or checkInstructorRole(myuser(request))==True or checkTARole(myuser(request))==True:
            allcourses=course.objects.all()
            allsections=section.objects.all()
            return render(request, "ViewAssignments.html",{"username": myuser(request), "allcour":allcourses, "allsect":allsections})
        else:
            return redirect("/Denied", {"username": myuser(request)})


    def post(self, request):
        return render(request, "ViewAssignments.html",{"username": myuser(request)})


class EditAccount(View):
    def get(self, request):
        myuser = request.session["username"]
        if checkAdminRole(myuser) == True or checkInstructorRole(myuser) == True or checkTARole(myuser) == True:
            myuser = request.session["username"]
            myaccount=user.objects.get(email=myuser)
        else:
            return redirect("/Denied", {"username": myuser})

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
        return render(request, "denied.html",{"username": myuser(request)})

