from .test_case import TestCase
import unittest
import saga
import sys
import os
import fileutils
import StringIO

class TestCat(TestCase):
    def setUp(self):
        self.out = StringIO.StringIO()
        sys.stdout = self.out

    def test_cat(self):
        fileutils.cat(["/proc/version"])
        output = self.out.getvalue().strip()
        
        self.assertRegexpMatches(output, "^Linux")

    def test_ssh_cat(self):
        fileutils.cat(["ssh://localhost/proc/version"])
        output = self.out.getvalue().strip()
        
        self.assertRegexpMatches(output, "^Linux")

    def test_cat_multiple_file(self):
        fileutils.cat(["/proc/version", "/proc/version"])
        output = self.out.getvalue().strip()

        self.assertRegexpMatches(output, "^Linux.*?\n*Linux")
        
    def test_cat_unknow_file(self):
        fileutils.cat(["/unknown"])
        output = self.out.getvalue().strip()

        self.assertEqual(output, "file://localhost/unknown does not exist")
