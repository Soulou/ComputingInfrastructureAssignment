# -*- coding: utf-8 -*-
import saga
import getpass
from .file import *

def _build_ssh_session(user):
    ctx = saga.Context("ssh")
    ctx.user_id = user
    session = saga.Session()
    session.add_context(ctx)

def copy(files, dest, verbose=False, force=False, user=getpass.getuser()):
    session = _build_ssh_session(user)

    dest_url = saga.Url(dest)
    src_urls = []
    for f in files:
        src_urls += [saga.Url(f)]

    dest = File(session, dest)
    if not dest.is_dir and len(files) > 1:
        raise InvalidCopyException(str(dest))

    for f in files:
        src = File(session, f)
        if verbose:
            print "Copy %s → %s" % (str(src), str(dest))
        try:
            src.copy_to(dest, force)
        except FileutilsException, e:
            print e

def cat(files, outfile=None, user=getpass.getuser()):
    session = _build_ssh_session(user)

    output = None
    out = ""
    if outfile != None:
        output = File(session, outfile, saga.filesystem.TRUNCATE)

    for _f in files:
        try:
            f = File(session, _f)
            if output != None:
                out += f.read()
            else:
                print f.read()
        except FileutilsException, e:
            print e
    
    if output != None:
        output.write(out)

def list(dir, user=getpass.getuser()):
    session = _build_ssh_session(user)
    _dir = File(session, dir)
    for file in _dir.list():
        print file

def remove(files, user=getpass.getuser()):
    session = _build_ssh_session(user)

    for _f in files:
        try:
            f = File(session, _f)
            f.remove()
        except FileutilsException, e:
            print e
    
