import unittest
import saga
import os
import fileutils
import sessions
import getpass

class SampleArgs:
    def __init__(self):
        self.certificate = None
        self.identity = None
        self.user = getpass.getuser()

class TestCase(unittest.TestCase):
    sessions.Factory.setup(SampleArgs())
    def session(self):
        return sessions.Factory.new()
