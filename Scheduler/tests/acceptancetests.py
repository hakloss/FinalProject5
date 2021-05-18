from django.test import TestCase, Client
from Scheduler.models import *


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

class ViewDeleteAccounts(TestCase):
    def setUp(self):
        self.client = Client()
        self.x = user(fname="Ed", lname="Minn", email="admin@email.com", role="admin", password="Admin1")
        self.x.save()
        self.y = user(fname="Ann", lname="Structor", email="instructor@email.com", role="Instructor",
                      password="Instructor1")
        self.y.save()
#       self.z = user(fname="George", lname="Washington", email="george@aol.com", role="TA", password="TA1")
#       self.z.save()

    def test_delete_success(self):
        session = self.client.session
        session['username'] = self.x.email
        session.save()

        xuser = self.client.get("/ViewAccounts/", {"account": self.y}, follow=True)
        r = self.client.post("/ViewAccounts/", {"account": xuser}, follow=True)
        self.assertEqual(r.context["successmsg"], "Account has been deleted")