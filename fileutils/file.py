# -*- coding: utf-8 -*-

from .exceptions import *

import re
import saga
import saga.filesystem
import os.path as path

class File:
    def __init__(self, session, url, mode = saga.filesystem.READ):
        '''
        session: saga.Session
        url: str
        '''
        self.session = session

        self.url = saga.Url(url)
        if self.url.scheme == "":
            url = "file://localhost%s" % path.abspath(url)
            self.url = saga.Url(url)

        if not re.match("^file|ssh|sftp|local$", self.url.scheme):
            raise BadProtocolException(self.url)

        try:
            self.fd = saga.filesystem.File(url, mode, session=self.session)
            self.is_dir = self.fd.is_dir()
            self.exist = True
        except saga.DoesNotExist, e:
            self.exist = False
            self.is_dir = False

    def __str__(self):
        '''
        ret str
        '''
        return str(self.url)

    def read(self):
        '''
        ret str
        '''
        if not self.exist:
            raise UnknownFileException(self)
        if self.is_dir:
            raise ReadDirectoryException(self)
        file_content = ""
        try:
            file_content = self.fd.read()
        except IOError:
            file_content = self.fd.read()
        return file_content

    def write(self, content):
        if self.is_dir:
            raise WriteDirectoryException(self)
        self.fd.write(content)

    def copy_to(self, dest, force=False):
        '''
        dest:  File
        force: bool
        '''
        if self.is_dir:
            raise CopySrcDirectoryException(dest)
        if not self.exist:
            raise UnknownFileException(self)

        if dest.is_dir:
            new_file_url = self._new_file_url(dest)
            tmp_file = File(self.session, new_file_url)
            if not tmp_file.exist or (tmp_file.exist and force):
                self.fd.copy(new_file_url)
            else:
                raise UnauthorizedOverrideException(self, new_file_url)
        elif not dest.exist or force:
            self.fd.copy(dest.url)
        else:
            raise UnauthorizedOverrideException(self, dest.url)

    def remove(self):
        if not self.exist:
            raise UnknownFileException(self)
        if self.is_dir:
            raise RemoveDirectoryException(self)

        self.fd.remove()

    def list(self):
        if not self.exist:
            raise UnknownFileException(self)
        if not self.is_dir:
            raise ListFileException(self)

        dir = saga.filesystem.Directory(self.url)
        for entry in dir.list():
            yield entry

    def _new_file_url(self, dest):
        '''
        dest: File
        ret:  str``
        '''
        return "%s/%s" % (dest.url, path.basename(self.url.path))
