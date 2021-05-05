from django.test import TestCase, Client
import unittest
from Scheduler import functions
from Scheduler.models import *


# Create your tests here.

class TestDuplicateAccount(unittest.TestCase):
    def setUp(self):
        self.acc = user(fname="Haley", lname="K", email="hajaroch@uwm.edu", password="pass")
        self.acc2 = user(fname="Haley", lname="K", email="hajaroch@uwm.edu", password="pass")

    def test_duplicate(self):
        print(self.acc.email)
        self.assertEqual(functions.duplicateUserCheck("hajaroch@uwm.edu"), True, msg="Account already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateUserCheck("test@email.com"), False, msg="Not a duplicate")


class TestDuplicateCourse(unittest.TestCase):
    def setUp(self):
        self.c = course(classname="CS361")
        print(self.c)

    def test_duplicate(self):
        self.assertEqual(functions.duplicateCourseCheck(self.c.classname), True, msg="Course already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateCourseCheck("CS351"), False, msg="Not a duplicate")


class TestDuplicateSection(unittest.TestCase):
    def setUp(self):
        self.c = course(classname="CS361")
        self.s = section(number="201", time="10:30", course=self.c)

    def test_duplicate(self):
        self.assertEqual(functions.duplicateSectionCheck(self.s.number, self.s.time, self.s.course), True,
                         msg="Section already exists")

    def test_differentSection(self):
        self.assertEqual(functions.duplicateSectionCheck("903", "12:00", self.s.course), False, msg="Not a duplicate")


# ACCEPTANCE TESTS

class Login(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="Haley", lname="K", email="test@email.com", password="password", role="admin",
                      address="123 street",
                      city="Milwaukee", state="WI", zip="55555", pphone="555-555-5555", wphone="555-555-5555")
        self.x.save()

    def test_validLogin(self):
        r = self.client.post('/', {"username": self.x.email, "password": self.x.password}, follow=True)
        self.assertEqual("/Home", r.redirect_chain[0][0])

    def test_badPassword(self):
        r = self.client.post('/', {"username": self.x.email, "password": "blah"}, follow=True)
        self.assertEqual(r.context["badmsg"], "Please enter a valid password")

    def test_badUsername(self):
        r = self.client.post('/', {"username": "email", "password": self.x.password}, follow=True)
        self.assertEqual(r.context["badmsg"], "Please enter a valid username")


class CreateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="Haley", lname="K", email="test@email.com", password="password", role="admin",
                      address="123 street",
                      city="Milwaukee", state="WI", zip="55555", pphone="555-555-5555", wphone="555-555-5555")
        self.x.save()

    def test_validAccount(self):
        r = self.client.post("/CreateAccount/", {"fname": "Hallllley", "lname": "Kloss", "email": "thing@uwm.edu",
                                               "password": "password", "role": "admin"}, follow=True)
        self.assertEqual(r.context["successmsg"], "Account has been created")
"""
    def test_invalidAccount(self):
        r = self.client.post("/CreateAccount/", {"fname": "Hallllley", "lname": "Kloss", "email": "thing",
                                               "password": "password", "role": "instructor"}, follow=True)

        self.assertEqual(r.context["badmsg"], "Please enter a valid email")
"""


class EditAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="Haley", lname="K", email="test@email.com", password="password", role="admin", address="123 street",
                      city="Milwaukee", state="WI", zip="55555", pphone="555-555-5555", wphone="555-555-5555")
        self.x.save()

    def test_validEdit(self):
        session = self.client.session
        session['username'] = self.x.email
        session.save()

        r = self.client.post("/EditAccount/", {"fname": "Hallllley", "lname":"Kloss", "email":self.x.email, "password":self.x.password, "role":self.x.role}, follow=True)
        print(r.context)
        self.assertEqual(r.context["successmsg"], "Account has been updated")
        self.assertEqual(r.context["account"].fname, "Hallllley")
        self.assertEqual(r.context["account"].lname, "Kloss")





