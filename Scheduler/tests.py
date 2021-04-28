from django.test import TestCase, Client
import unittest
from Scheduler import functions
from Scheduler.models import *
# Create your tests here.

class TestDuplicateAccount(unittest.TestCase):
    def setUp(self):
        self.acc=user(fname="Haley", lname="K",email="hajaroch@uwm.edu", password="pass")

    def test_duplicate(self):
        self.assertEqual(functions.duplicateUserCheck(self.acc.email), True, msg="Account already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateUserCheck("test@email.com"), False, msg="Not a duplicate")

class TestDuplicateCourse(unittest.TestCase):
    def setUp(self):
        self.c=course(classname="CS361")
        print(self.c)
    def test_duplicate(self):
        self.assertEqual(functions.duplicateCourseCheck(self.c.classname), True, msg="Course already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateCourseCheck("CS351"), False, msg="Not a duplicate")

class TestDuplicateSection(unittest.TestCase):
    def setUp(self):
        self.c=course(classname="CS361")
        self.s=section(number="201", time="10:30", course=self.c)

    def test_duplicate(self):
        self.assertEqual(functions.duplicateSectionCheck(self.s.number, self.s.time, self.s.course), True, msg="Section already exists")

    def test_differentSection(self):
        self.assertEqual(functions.duplicateSectionCheck("903", "12:00", self.s.course), False, msg="Not a duplicate")


#ACCEPTANCE TESTS

class Login(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(email="test@email.com", password="password")
        self.x.save()

    def test_validLogin(self):
        r = self.client.post('/', {"username": self.x.email, "password": self.x.password}, follow=True)
        self.assertEqual("/Home", r.redirect_chain[0][0])
        
    def test_badPassword(self):
        r = self.client.post('/', {"username": self.x.email, "password": self.x.password}, follow=True)
        self.assertEqual(r.context["badmsg"], "Please enter a valid password")

    def test_badUsername(self):
        r = self.client.post('/', {"username": self.x.email, "password": self.x.password}, follow=True)
        self.assertEqual(r.context["badmsg"], "Please enter a valid username")

class CreateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="Haley", lname="K", email="test@email.com", password="password", role="admin", address="123 street",
                      city="Milwaukee", state="WI", zip="55555", pphone="555-555-5555", wphone="555-555-5555")
        self.x.save()

    def test_validAccount(self):
        #r = self.client.post('/CreateAccount/', {"fname"=self.x.fname,"lname"=self.x.lname, "email"=self.x.email, "password"=self.x.password, "role"=self.x.role, "address"=self.x.address, "city"=self.x.city, "state"=self.x.state, "zip"=self.x.zip, "pphone"=self.x.pphone, "wphone"=self.x.wphone}, follow=True)
        self.assertEqual(r.context["successmsg"], "Account has been created")

    def test_invalidAccount(self):
       # r = self.client.post("/CreateAccount/", {"fname"= self.x.fname, "lname"= self.x.lname, "email"= "email", "password"= self.x.password, "role"= self.x.role, "address"= self.x.address, "city"= self.x.city, "state"= self.x.state, "zip"= self.x.zip, "pphone"= self.x.pphone, "wphone"=self.x.wphone}, follow=True)
        self.assertEqual(r.context["badmsg"], "Please enter a valid email")