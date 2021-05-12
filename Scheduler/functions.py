from django.shortcuts import render, redirect
from Scheduler.models import *

def duplicateUserCheck(email):
    allaccounts = user.objects.all()
    for i in allaccounts:
        if i.email==email:
            return True
    return False

def duplicateCourseCheck(classname):
    allcourses = course.objects.all()
    for i in allcourses:
        if i.classname==classname:
            return True
    return False

def duplicateSectionCheck(number,time,course):
    allsections = section.objects.all()
    for i in allsections:
        if i.number==number and i.time==time and i.course==course:
            return True
    return False


def validateEmail(email):
    at="@"
    dot="."
    if at in email and dot in email:
        return True
    return False


def checkAdminRole(email):
    account = user.objects.get(email=email)
    if (account.role=="admin" or account.role=="Admin"):
        return True
    return False

def checkInstructorRole(email):
    account = user.objects.get(email=email)
    if (account.role=="instructor" or account.role=="Instructor"):
        return True
    return False


def checkTARole(email):
    account = user.objects.get(email=email)
    if (account.role=="ta" or account.role=="TA"):
        return True
    return False

def getAccount(request):
    myuser = request.session["username"]
    myaccount = user.objects.get(email=myuser)
    return myaccount

def sectionList(xcourse):
    sectionlist = []
    courseobj=course.objects.get(classname=xcourse)
    allsections = (section.objects.values())
    for i in allsections:
        if i.get("course_id","default")==courseobj.id:
            sectionlist.append(i["number"])
    return sectionlist

def courseList():
    allcourses = (course.objects.values())
    courselist = []
    for i in allcourses:
        courselist.append(i['classname'])
    return courselist

def TAlist():
    allusers = (user.objects.values())
    talist = []
    for i in allusers:
        if i.get("role", "default") == "ta" or i.get("role", "default") == "TA":
            taname = i.get("email", "default")
            talist.append(taname)
    print(talist)
    return talist

def maxSectionTally(taEmail):
    myuser=user.objects.get(email=taEmail)
    if myuser.remainingSection>0:
        myuser.remainingSection-=1
        myuser.save()
        print(myuser.remainingSection)

def myuser(request):
    return request.session["username"]