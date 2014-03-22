import unittest
import saga
import os
import fileutils

class TestCase(unittest.TestCase):
    _session = None
    def session(self):
        if TestCase._session == None:
            TestCase._session = saga.Session()
            ctx = saga.Context("ssh")
            TestCase._session.add_context(ctx)
        return TestCase._session
