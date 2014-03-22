from .test_case import TestCase
import unittest
import saga
import os
import fileutils

class TestFileCopy(TestCase):
    @classmethod
    def remove_test_files(cls):
        for file in ["/tmp/hosts", "/tmp/new_file"]:
            try:
                os.remove(file)
            except Exception, e:
                pass

    @classmethod
    def setUpClass(cls):
        TestFileCopy.remove_test_files()
    def tearDown(self):
        TestFileCopy.remove_test_files()

    def test_copy_to_dir(self):
        dst = fileutils.File(self.session(), "ssh://localhost/tmp")
        src = fileutils.File(self.session(), "/etc/hosts")
        src.copy_to(dst)

        check_dst = fileutils.File(self.session(), "ssh://localhost/tmp/hosts")
        self.assertTrue(check_dst.exist)
        self.assertFalse(check_dst.is_dir)

        dst = fileutils.File(self.session(), "ssh://localhost/tmp")
        self.assertRaises(
            fileutils.UnauthorizedOverrideException,
            src.copy_to, dst
        )

        dst = fileutils.File(self.session(), "ssh://localhost/tmp/hosts")
        self.assertRaises(
            fileutils.UnauthorizedOverrideException,
            src.copy_to, dst
        )

    def test_copy_to_new_file(self):
        src = fileutils.File(self.session(), "/etc/hosts")
        dst = fileutils.File(self.session(), "ssh://localhost/tmp/new_file")

        src.copy_to(dst)
        check_dst = fileutils.File(self.session(), "ssh://localhost/tmp/new_file")
        self.assertFalse(dst.exist)
        self.assertTrue(check_dst.exist)

    def test_copy_to_force(self):
        src = fileutils.File(self.session(), "/etc/hosts")
        dst = fileutils.File(self.session(), "ssh://localhost/tmp/new_file")
        src.copy_to(dst)

        # Rewrite the file
        src.copy_to(dst, True)

        # Again but asking to write it in the parent dir
        dst = fileutils.File(self.session(), "ssh://localhost/tmp")
        src.copy_to(dst, True)

