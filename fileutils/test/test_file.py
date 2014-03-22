from .test_case import TestCase
import unittest
import saga
import os
import fileutils

class TestSequenceFunctions(TestCase):
    def test_new_dir(self):
        f = fileutils.File(self.session(), "file://localhost/tmp")
        self.assertTrue(f.is_dir)
        self.assertTrue(f.exist)

    def test_new_file(self):
        f = fileutils.File(self.session(), "file://localhost/etc/hosts")
        self.assertFalse(f.is_dir)
        self.assertTrue(f.exist)

    def test_new_unknow_file(self):
        f = fileutils.File(self.session(), "file://localhost/tmp/not_a_file")
        self.assertFalse(f.is_dir)
        self.assertFalse(f.exist)

    def test_ssh_file(self):
        f = fileutils.File(self.session(), "ssh://localhost/tmp")
        self.assertTrue(f.is_dir)
        self.assertTrue(f.exist)

    def test_str(self):
        f = fileutils.File(self.session(), "ssh://localhost/tmp")
        self.assertEqual(str(f.url), str(f))

    def test_invalid_scheme(self):
        self.assertRaises(
            fileutils.BadProtocolException,
            fileutils.File, self.session(), "xyz://localhost/tmp"
        )

    def test_local_file(self):
        f = fileutils.File(self.session(), "/etc/hosts")
        self.assertEqual(str(f.url), "file://localhost/etc/hosts")

    def test_local_relative_file(self):
        f = fileutils.File(self.session(), "..")
        path = os.path.abspath(os.getcwd() + "/..")
        self.assertEqual(str(f.url), ("file://localhost%s" % path))
