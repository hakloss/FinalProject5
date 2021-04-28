from django.test import TestCase
import unittest
from Scheduler import functions
from Scheduler.models import *
# Create your tests here.

class TestDuplicateAccount(unittest.TestCase):
    def setUp(self):
        self.acc=user(email="hajaroch@uwm.edu", password="pass")

    def test_duplicate(self):
        self.assertEqual(functions.duplicateUserCheck(self.acc.email), True, msg="Account already exists")

    def test_noDuplicate(self):
        self.assertEqual(functions.duplicateUserCheck("test@email.com"), False, msg="Not a duplicate")

class TestDuplicateCourse(unittest.TestCase):
    def setUp(self):
        self.c=course(classname="CS361")

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


