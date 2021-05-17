from django.test import TestCase
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


    def test_duplicate(self):
        self.assertEqual(True, functions.duplicateUserCheck("hajaroch@uwm.edu"), msg="Account already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateUserCheck("email@email.com"), False, msg="Not a duplicate")


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

class TestMaxSectionTally(TestCase):
    def setUp(self):

        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="TA", password="fdsahjk")
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="TA", password="jhfkdjsalfhadis")
        self.z.save()

        self.c=course(classname="CS361")
        self.c.save()

        self.s=section(course=self.c, number="101", ta=self.y)
        self.s.save()
        self.s1 = section(course=self.c, number="102", ta=self.y)
        self.s1.save()
        self.s2 = section(course=self.c, number="103", ta=self.z)
        self.s2.save()

    def test_count(self):
        self.assertEqual(functions.maxSectionTally(self.y.email), 2, msg="should be the same")


class TestDecrement(TestCase):
    def setUp(self):

        self.y = user(fname="Joe", lname="Johnson", email="emailOne@password.com", role="TA", password="fdsahjk", maxsection=3, remainingSection=1)
        self.y.save()
        self.z = user(fname="Sam", lname="Brown", email="emailTwo@something.com", role="TA", password="jhfkdjsalfhadis", maxsection=1, remainingSection=0)
        self.z.save()

        self.c=course(classname="CS361")
        self.c.save()

        self.s=section(course=self.c, number="101", ta=self.y)
        self.s.save()
        self.s1 = section(course=self.c, number="102", ta=self.y)
        self.s1.save()
        self.s2 = section(course=self.c, number="103", ta=self.z)
        self.s2.save()

    def test_decrement(self):
        functions.deductSection(self.y.email)
        self.assertEqual(self.y.remainingSection, 0, msg="should be the same")

    def test_deductZero(self):
        functions.deductSection(self.z.email)
        self.assertEqual(self.z.remainingSection, 0, msg="should go below zero")


