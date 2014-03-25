# -*- coding: utf-8 -*-

import re
import os

class InvalidJob(Exception):
    def __init__(self, line):
        self.message = "Invalid job %s" % line

class Job:
    def __init__(self, line):
        # "JOB" "LABEL" "command", "arg1 arg2"
        job_array = re.split(" ", line, 3)
        if len(job_array) != 4:
            raise InvalidJob(line)

        self.label = job_array[1]
        self.cmd = job_array[2]
        self.args = re.split(" ", job_array[3])

    def __eq__(self, other):
        return self.label == other.label
    def __hash__(self):
        return hash(self.label)
    def __str__(self):
        return "[%s] %s %s" % (self.label, self.cmd, self.args)

    def run(self):
        args = ' '.join(map(str,self.args))
        print "→ Run job %s: '%s %s'" % (self.label, self.cmd, args)
        return os.system("%s %s" % (self.cmd, args))
