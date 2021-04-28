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


