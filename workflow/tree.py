# -*- coding: utf-8 -*-

import re
from .job import Job
from .relation import Relation

class ExecutionError(Exception):
    def __init__(self, job):
        self.message = "An error occured for job %s", job

class CycleWorkflowError(Exception):
    def __init__(self, cycle):
        cycle_str = ""
        for node in cycle:
            cycle_str += "%s\n" % node
        self.message = "Your workflow is cyclic:\n%s" % cycle_str

class Node:
    def __init__(self, label, job, parent=None):
        self.label = label
        self.job = job
        self.children = set()
        self.parents = set()
        if parent != None:
            self.parents.add(parent)
    def __hash__(self):
        return hash(self.label)
    def __eq__(self, other):
        if other == None:
            return False
        return self.label == other.label
    def is_orphan(self):
        return len(self.parents) == 0 and len(self.children) == 0
    def is_root(self):
        return len(self.parents) == 0
    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, node):
        self.children.add(node)

    def add_parent(self, node):
        self.parents.add(node)

    def __str__(self):
        children_str = "(leaf)"
        if not self.is_leaf():
            children_str = "→ ["
            for c in self.children:
                children_str += c.label + ", "
            children_str += "\b\b]"

        parents_str = "(root)"
        if not self.is_root():
            labels_str = "["
            for p in self.parents:
                labels_str += "%s, " % p.label
            labels_str += "\b\b]"
            parents_str = "(parents: %s)" % labels_str

        orphan_str = ""
        if self.is_orphan():
            orphan_str = "(orphan)"

        return "[%s] %s %s %s" % (self.label, children_str, parents_str, orphan_str)

class Tree:
    def __init__(self, file):
        self.jobs = set()
        self.relations = set()
        self.input_file = file
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if re.match("^JOB", line):
                    self.add_job(line)
                if re.match("^PARENT", line):
                    self.add_relation(line)
        self.build_tree()

        cycle = self.cycle()
        if cycle != None:
            raise CycleWorkflowError(cycle)

    def add_job(self, line):
        job = Job(line)
        self.jobs.add(job)

    def add_relation(self, line):
        # Their can be several relations in one line
        # PARENT A CHILD B C creates A → B and A → C
        relations = Relation.parse_relations(line)
        for r in relations:
            self.relations.add(r)
        
    def build_tree(self):
        self.nodes = set()
        for r in self.relations:
            node = self._find_node(r.src)
            if node == None:
                job = self._find_job(r.src)
                node = Node(r.src, job)
                self.nodes.add(node)

        for r in self.relations:
            node = self._find_node(r.src)
            dst = self._find_node(r.dst)

            # If a destination hasn't been added to the tree, it's a leaf
            if dst == None:
                job = self._find_job(r.dst)
                dst = Node(r.dst, job, node)
                self.nodes.add(dst)
            else:
                dst.add_parent(node)
            node.add_child(dst)

        # Create orphan nodes
        for j in self.jobs:
            node = self._find_node(j.label)
            if node == None:
                node = Node(j.label, j)
                self.nodes.add(node)

    def __str__(self):
        res = "" 
        for node in self.nodes:
            res += "%s\n" % node
        return res


    def _find_node(self, label):
        for n in self.nodes:
            if n.label == label:
                return n
        return None

    def _find_job(self, label):
        for j in self.jobs:
            if j.label == label:
                return j
        return None

    def cycle(self):
        todo = self.nodes.copy()
        while todo:
            node = todo.pop()
            stack = [node]
            while stack:
                top = stack[-1]
                for node in node.children:
                    if node in stack:
                        return stack[stack.index(node):]
                    if node in todo:
                        stack.append(node)
                        todo.remove(node)
                        break
                else:
                    stack.pop()
        return None

    def run(self):
        to_remove = set()
        for n in self.nodes:
            if n.is_orphan():
                ret = n.job.run()
                if ret != 0:
                    raise ExecutionException(n.job)
                to_remove.add(n)
        while len(to_remove) > 0:
            self.remove_node(to_remove.pop())
        
        while len(self.nodes) > 0:
            for n in self.nodes:
                if n.is_leaf():
                    n.job.run()
                    to_remove.add(n)

            while len(to_remove) > 0:
                self.remove_node(to_remove.pop())

    def remove_node(self, node):
        for n in self.nodes:
            if node in n.children:
                n.children.remove(node)
        self.nodes.remove(node)
                

