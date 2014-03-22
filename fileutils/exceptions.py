# -*- coding: utf-8 -*-

class FileutilsException(Exception):
    pass

class BadProtocolException(FileutilsException):
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return "scheme \"%s\" of \"%s\" is not implemented, use file:// or ssh://" % (self.url.scheme, self.url)
class CopySrcDirectoryException(FileutilsException):
    def __init__(self, src, dest):
        self.src = src
        self.dst = dest
    def __str__(self):
        return "can't copy %s → %s, source file is a is a directory" % str(self.src), str(self.dst)
class InvalidCopyException(FileutilsException):
    def __init__(self, dst):
        self.dst = dst
    def __str__(self):
        return "destination %s is a file, can't copy more than one source file" % str(self.dest)
class UnauthorizedOverrideException(FileutilsException):
    def __init__(self, old, new):
        self.old = old
        self.new = new
    def __str__(self):
        return "%s would override %s, use -f if you're sure" % (str(self.old), self.new) 
class UnknownFileException(FileutilsException):
    def __init__(self, file):
        self.file = file
    def __str__(self):
        return "%s does not exist" % str(self.file)
class ListFileException(FileutilsException):
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return "%s is a file, can't list it" % self.dir
class ReadDirectoryException(FileutilsException):
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return "%s is a directory, can't read it" % self.dir
class WriteDirectoryException(FileutilsException):
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return "%s is a directory, can't write it" % self.dir
class RemoveDirectoryException(FileutilsException):
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return "%s is a directory, can't remove it" % self.dir
