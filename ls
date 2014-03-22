#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import saga
import saga.filesystem
import argparse
import getpass
import fileutils
import sessions

'''
   SAGA_VERBOSE=# for Debug
'''

def main():
    parser = argparse.ArgumentParser(description='List files in directory using saga API')
    parser.add_argument('--identity', '-i', metavar='private_key', type=str, nargs="?",
        help='custom private key for SSH connection')
    parser.add_argument('--certificate', '-c', metavar='certificate', type=str, nargs="?",
        help='enable GSISSH connection, specify certificate to use')
    parser.add_argument('--user', '-u', metavar='user', type=str, nargs=1, default=getpass.getuser(),
        help='user to use for ssh connections')
    parser.add_argument('dir', metavar='dir', type=str, nargs=1,
        help='directory to explore')
    args = parser.parse_args()
    sessions.Factory.setup(args)
    
    try:
        fileutils.list(args.dir[0])
        return 0
    except (fileutils.FileutilsException), e:
        print "Exception of ls: %s" % str(e)
    except saga.SagaException, ex:
        print "A sage exception occured: (%s) %s " % (ex.type, (str(ex)))
        print " \n*** Backtrace:\n %s" % ex.traceback
        return -1

if __name__ == "__main__":
    sys.exit(main())
