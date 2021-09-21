from visualize import *

class Node:
    def __init__(self, val, fch=None, sch=None, tch=None):
        self.val = val
        self.fch = fch
        self.sch = sch
        self.tch = tch

root = Node('a', Node('b'), Node('c', Node('e'), Node('f'), Node('g')), Node('d'))

Structure(root).print()
