from .test_case import TestCase
import unittest
import saga
import sys
import os
import fileutils
import StringIO

class TestRm(TestCase):
    def setUp(self):
        self.out = StringIO.StringIO()
        sys.stdout = self.out

    def test_rm(self):
        fileutils.copy(["/etc/hosts"], "/tmp/hosts")
        fileutils.copy(["/etc/hosts"], "/tmp/hosts2")
        fileutils.remove(["/tmp/hosts", "/tmp/hosts2"])

        f = fileutils.File(self.session(), "/tmp/hosts")
        self.assertFalse(f.exist)
        f = fileutils.File(self.session(), "/tmp/hosts2")
        self.assertFalse(f.exist)

    def test_rm_unknown_file(self):
        fileutils.remove(["/unknown"])
        output = self.out.getvalue().strip()
        self.assertRegexpMatches(output, "does not exist$")

    def test_rm_dir(self):
        fileutils.remove(["/tmp"])
        output = self.out.getvalue().strip()
        self.assertRegexpMatches(output, "is a directory, can't remove it$")
