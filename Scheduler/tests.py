from django.test import TestCase, Client
import unittest
from Scheduler import functions
from Scheduler.models import *


# Create your tests here.
class TestGetLastName(TestCase):
    def setUp(self):
        self.x = "John Joe"
        self.y = "Jeff"
        self.z = "Sara Johnson"

    def test_name(self):
        self.assertEqual(functions.getLastName(self.x), "Joe")

    def test_oneName(self):
        self.assertEqual(functions.getLastName(self.y), "Jeff")

    def test_firstName(self):
        self.assertFalse(functions.getLastName((self.z)) == "Sara")




class TestDuplicateAccount(TestCase):
    def setUp(self):
        self.acc = user(fname="Haley", lname="K", email="hajaroch@uwm.edu", password="pass", role="TA")
        self.acc.save()
        self.acc2 = user(fname="Haley", lname="K", email="hajaroch@uwm.edu", password="pass", role="TA")

    def test_duplicate(self):
        self.assertEqual(True, functions.duplicateUserCheck("hajaroch@uwm.edu"), msg="Account already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateUserCheck(self.acc2.email), False, msg="Not a duplicate")


class TestDuplicateCourse(unittest.TestCase):
    def setUp(self):
        self.c = course(classname="CS361")
        self.c.save()

    def test_duplicate(self):
        self.assertEqual(functions.duplicateCourseCheck(self.c.classname), True, msg="Course already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateCourseCheck("CS351"), False, msg="Not a duplicate")


class TestDuplicateSection(unittest.TestCase):
    def setUp(self):
        self.c = course(classname="CS361")
        self.c.save()
        self.s = section(number="201", time="10:30", course=self.c)
        self.s.save()

    def test_duplicate(self):
        self.assertEqual(functions.duplicateSectionCheck(self.s.number, self.s.time, self.s.course), True,
                         msg="Section already exists")

    def test_differentSection(self):
        self.assertEqual(functions.duplicateSectionCheck("903", "12:00", self.s.course), False, msg="Not a duplicate")


class TestValidateEmail(unittest.TestCase):
    def setUp(self):
        self.good="haley@uwm.edu"
        self.bad="fdgsdfg"

    def test_valid(self):
        self.assertEqual(functions.validateEmail(self.good), True, msg="should be valid")

    def test_invalid(self):
        self.assertEqual(functions.validateEmail(self.bad), False, msg="should be invalid")

class TestCheckAdminAccount(TestCase):
    def setUp(self):
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk")
        self.x.save()
        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="instructor", password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="ta", password="jhfkdjsalfhadis")
        self.z.save()

    def test_admin(self):
        self.assertTrue(functions.checkAdminRole(self.x.email))

    def test_instructor(self):
        self.assertFalse(functions.checkAdminRole(self.y.email))

    def test_ta(self):
        self.assertFalse(functions.checkAdminRole(self.z.email))

class TestCheckInstructorAccount(TestCase):
    def setUp(self):
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk")
        self.x.save()
        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="instructor", password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="ta", password="jhfkdjsalfhadis")
        self.z.save()

    def test_admin(self):
        self.assertFalse(functions.checkInstructorRole(self.x.email))

    def test_instructor(self):
        self.assertTrue(functions.checkInstructorRole(self.y.email))

    def test_ta(self):
        self.assertFalse(functions.checkInstructorRole(self.z.email))

class TestCheckTAAccount(TestCase):
    def setUp(self):
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk")
        self.x.save()
        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="instructor", password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="ta", password="jhfkdjsalfhadis")
        self.z.save()

    def test_admin(self):
        self.assertFalse(functions.checkTARole(self.x.email))

    def test_instructor(self):
        self.assertFalse(functions.checkTARole(self.y.email))

    def test_ta(self):
        self.assertTrue(functions.checkTARole(self.z.email))

class TestTAList(TestCase):
    def setUp(self):
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk")
        self.x.save()
        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="TA", password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="TA", password="jhfkdjsalfhadis")
        self.z.save()

    def test_retrieveTA(self):
        self.assertEqual(functions.TAlist(), ["emailOne@password.com","emailTwo@something.com"], msg="should be the same")

    def test_Excludeother(self):
        self.assertFalse("email@email.com" in functions.TAlist(), msg="admin should not be in list")

class TestcourseList(TestCase):
    def setUp(self):
        self.c1 = course(classname="301")
        self.c1.save()
        self.c2 = course(classname="302")
        self.c2.save()
        self.c3 = course(classname="303")
        self.c3.save()

    def test_couselist(self):
        self.assertEqual(functions.courseList(), ["301", "302", "303"], msg="should be the same")

class TestSectionList(TestCase):
    def setUp(self):
        self.c1 = course(classname="301")
        self.c1.save()
        self.c2 = course(classname="302")
        self.c2.save()
        self.c3 = course(classname="303")
        self.c3.save()

        self.s1 = section(course=self.c1, number="101")
        self.s1.save()
        self.s2 = section(course=self.c1, number="102")
        self.s2.save()
        self.s3 = section(course=self.c2, number="101")
        self.s3.save()

    def test_sectionlist(self):
        self.assertEqual(functions.sectionList("301"), ["101", "102"], msg="should be the same")

class TestRemainingSection(TestCase):
    def setUp(self):
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk", maxsection=3, remainingSection=3)
        self.x.save()

    def test_decrement(self):
        functions.maxSectionTally(self.x.email)
        print(self.x.remainingSection)
        self.assertEqual(self.x.remainingSection, 2, msg="should be the same")



""""
class TestgetAccount(TestCase):
    def setUp(self):
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk")
        self.x.save()

        session = self.client.session
        session['username'] = self.x.email
        session.save()

    def test_returnAccount(self):
        r = self.client.post('/', {"username": self.x.email}, follow=True)
        self.assertEqual(functions.getAccount(r), "email@email.com", msg="returns primary key for acount")
"""
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
        self.assertEqual(r.context["badmsg"], "Please enter valid login credentials")

    def test_badUsername(self):
        r = self.client.post('/', {"username": "email", "password": self.x.password}, follow=True)
        self.assertEqual(r.context["badmsg"], "Please enter valid login credentials")


class CreateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="Haley", lname="K", email="test@email.com", password="password", address="123 street",
                      city="Milwaukee", state="WI", zip="55555", pphone="555-555-5555", wphone="555-555-5555")
        self.x.save()

    def test_validAccount(self):
        session = self.client.session
        session['role'] = 'Admin'
        session.save()

        r = self.client.post("/CreateOther/", {"fname": "Hallllley", "lname": "Kloss", "email": "thing@uwm.edu",
                                               "password": "password"}, follow=True)
        self.assertEqual(r.context["successmsg"], "Account has been created")

    def test_invalidAccount(self):
        session = self.client.session
        session['role'] = 'Instructor'
        session.save()

        r = self.client.post("/CreateOther/", {"fname": "Hallllley", "lname": "Kloss", "email": "thing",
                                               "password": "password"}, follow=True)

        self.assertEqual(r.context["badmsg"], "Please enter a valid email")

    def test_validAccountTA(self):
        session = self.client.session
        session['role'] = 'TA'
        session.save()

        r = self.client.post("/CreateOther/", {"fname": "Hallllley", "lname": "Kloss", "email": "thing@uwm.edu",
                                               "password": "password"}, follow=True)
        self.assertEqual(r.context["successmsg"], "Account has been created")

    def test_invalidAccountTA(self):
        session = self.client.session
        session['role'] = 'TA'
        session.save()

        r = self.client.post("/CreateOther/", {"fname": "Hallllley", "lname": "Kloss", "email": "thing",
                                               "password": "password"}, follow=True)

        self.assertEqual(r.context["badmsg"], "Please enter a valid email")



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
        self.assertEqual(r.context["successmsg"], "Account has been updated")
        self.assertEqual(r.context["account"].fname, "Hallllley")
        self.assertEqual(r.context["account"].lname, "Kloss")


class HomeRedirect(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="John", lname="Smith", email="email@email.com", role="admin", password="fdjhska;afds;hjk")
        self.x.save()
        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="Instructor",
                      password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="TA", password="jhfkdjsalfhadis")
        self.z.save()

    def test_adminHome(self):
        session = self.client.session
        session['username'] = self.x.email
        session.save()
        r = self.client.post("/Home",{"account":self.x, "username":self.x.email}, follow=True)
        self.assertRedirects(r, '/AdminHome/',status_code=301, target_status_code=200, fetch_redirect_response=True)

    def test_instructorHome(self):
        session = self.client.session
        session['username'] = self.y.email
        session.save()
        r = self.client.get("/Home",{"account":self.y, "username":self.y.email}, follow=True)
        self.assertRedirects(r, '/InstructorHome/',status_code=301, target_status_code=200, fetch_redirect_response=True)

    def test_taHome(self):
        session = self.client.session
        session['username'] = self.z.email
        session.save()
        r = self.client.get("/Home",{"account":self.z, "username":self.z.email}, follow=True)
        self.assertRedirects(r, '/TAHome/',status_code=301, target_status_code=200, fetch_redirect_response=True)

class PagePermissions(TestCase):
    def setUp(self):
        self.client = Client()
        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="Instructor",
                      password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="TA", password="jhfkdjsalfhadis")
        self.z.save()
        self.s = user(email="strangerdanger@something.com")
        self.s.save()

    def test_TApermissions(self):
        session = self.client.session
        session['username'] = self.z.email
        session.save()
        r = self.client.get("/CreateAccount",{"account":self.z, "username":self.z.email}, follow=True)
        self.assertRedirects(r, '/Denied/',status_code=301, target_status_code=200, fetch_redirect_response=True)

        r2 = self.client.get("/AddSection", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r2, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r3 = self.client.get("/AdminHome", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r3, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r4 = self.client.get("/AssignTA", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r4, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r5 = self.client.get("/CreateCourse", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r5, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r6 = self.client.get("/CreateOther", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r6, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r7 = self.client.get("/CreateTA", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r7, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r8 = self.client.get("/InstructorHome", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r8, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r9 = self.client.get("/SelectCourse", {"account": self.z, "username": self.z.email}, follow=True)
        self.assertRedirects(r9, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

    def test_Instructorpermissions(self):
        session = self.client.session
        session['username'] = self.y.email
        session.save()
        r = self.client.get("/CreateAccount",{"account":self.y, "username":self.y.email}, follow=True)
        self.assertRedirects(r, '/Denied/',status_code=301, target_status_code=200, fetch_redirect_response=True)

        r2 = self.client.get("/AddSection", {"account": self.y, "username": self.y.email}, follow=True)
        self.assertRedirects(r2, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r3 = self.client.get("/AdminHome", {"account": self.y, "username": self.y.email}, follow=True)
        self.assertRedirects(r3, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r5 = self.client.get("/CreateCourse", {"account": self.y, "username": self.y.email}, follow=True)
        self.assertRedirects(r5, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r6 = self.client.get("/CreateOther", {"account": self.y, "username": self.y.email}, follow=True)
        self.assertRedirects(r6, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r7 = self.client.get("/CreateTA", {"account": self.y, "username": self.y.email}, follow=True)
        self.assertRedirects(r7, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r8 = self.client.get("/TAHome", {"account": self.y, "username": self.y.email}, follow=True)
        self.assertRedirects(r8, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

    def test_StrangerPermissions(self):
        session = self.client.session
        session['username'] = self.s.email
        session.save()
        r = self.client.get("/ViewAccounts",{"account":self.s, "username":self.s.email}, follow=True)
        self.assertRedirects(r, '/Denied/',status_code=301, target_status_code=200, fetch_redirect_response=True)

        r2 = self.client.get("/ViewAssignments", {"account": self.s, "username": self.s.email}, follow=True)
        self.assertRedirects(r2, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r3 = self.client.get("/EditAccount", {"account": self.s, "username": self.s.email}, follow=True)
        self.assertRedirects(r3, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)

        r5 = self.client.get("/Home", {"account": self.s, "username": self.s.email}, follow=True)
        self.assertRedirects(r5, '/Denied/', status_code=301, target_status_code=200, fetch_redirect_response=True)



