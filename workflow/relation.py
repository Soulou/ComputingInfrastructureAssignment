# -*- coding: utf-8 -*-

import re

class InvalidRelation(Exception):
    def __init__(self, line):
        self.message = "Invalid relation %s" % line

class Relation:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst
    def __hash__(self):
        return hash(self.src) + hash(self.dst)
    def __str__(self):
        return "%s → %s" % (self.src, self.dst)
    
    @classmethod
    def parse_relations(cls, line):
        relations = []
        # "PARENT", "LABEL", "CHILD" "LABEL1 LABEL2"
        relation_arr = re.split(" ", line, 3)
        if len(relation_arr) != 4:
            raise InvalidRelation(line)

        for child in re.split(" ", relation_arr[3]):
            relations.append(Relation(relation_arr[1], child))

        return relations
