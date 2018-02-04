#! /usr/bin/env python

from itertools import chain
from collections import namedtuple
from string import ascii_uppercase

class Node(object):
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.edges = []
    def __repr__(self):
        return "N:" + str((self.x, self.y))


class Diamond(object):
    def __init__(self, x,y, u,r,d,l):
        for i in 'xyurld':
            setattr(self, i, locals()[i])


class Edge(object):
    Range=namedtuple('Range', ['min', 'max'])
    Range2=namedtuple('Range2', ['x','y'])
    def __init__(self, n0, n1):
        self.n0 = n0
        self.n1 = n1
    def __repr__(self):
        return "E:"+str([self.n0,self.n1])
    @property
    def range(self):
        return Edge.Range2(Edge.Range(self.n0.x, self.n1.x), 
                           Edge.Range(self.n0.y, self.n1.y))
    @property
    def horizontal(self):
        return self.n0.y == self.n1.y


class Puzzle(object):
    def __init__(self, nodes, diamonds):
        self.nodes = make_nodes(nodes)
        self.diamonds = make_diamonds(diamonds)
        self.edges = make_edges(nodes, diamonds)


def load_string(s):
    """ Given a multiline string in which 'o' denotes a node and 'A-Z'
        indicate diamonds, return a list of (x,y) tuples, one for each 
        node and a list of (x,y,u,l,d,r) tuples for each diamond.
    """
    nodes = []
    diamonds = {}
    for y, line in enumerate(s.splitlines()):
        if ':' in line:
            diamonds.setdefault(line[0], [None]*6)[2:6] = (int(i) for i in line.split(':')[1].split(','))
            continue
        for x, c in enumerate(line):
            if c == 'o':
                nodes.append((x,y))
            elif c in ascii_uppercase:
                diamonds.setdefault(c, [None]*6)[0:2] = (x,y)
    return nodes, sorted(diamonds.values())


def make_nodes(nodes):
    """Given a list of (x,y) tuples, return a map: (x,y)->Node(x,y)"""
    return {i:Node(*i) for i in nodes}


def make_diamonds(diamonds):
    return {(x,y):Diamond(x,y,u,r,d,l) for x,y,u,r,d,l in diamonds}


def make_edge(n1, n2):
    """Given two nodes, create an edge connecting them"""
    e = Edge(n1, n2) 
    n1.edges.append(e)
    n2.edges.append(e)
    return e


def make_edges(nodes, diamonds):
    edges = []

    by_col = sorted(chain(nodes, diamonds))
    for idx, val in enumerate(by_col[:-1]):
        next_val = by_col[idx+1]
        if val in diamonds or next_val in diamonds:
            continue
        if val[0] == next_val[0]:
            e = make_edge(nodes[val], nodes[next_val])
            edges.append(e)

    by_row = sorted(chain(nodes, diamonds), key=lambda x:(x[1], x[0]))
    for idx, val in enumerate(by_row[:-1]):
        next_val = by_row[idx+1]
        if val in diamonds or next_val in diamonds:
            continue
        if val[1] == next_val[1]:
            e = make_edge(nodes[val], nodes[next_val])
            edges.append(e)
    return edges


def edges_cross(e_h, e_v):
    """Determine if a horizontal and vertical edge overlap"""
    assert(e_h.horizontal)
    assert(not e_v.horizontal)
    h = e_h.range
    v = e_v.range
    # If the column (x) of the vertical edge is strictly within the horizontal 
    # range of the horizontal edge, and the row (y) of the horizontal edge is 
    # strictly within the vertical range of the vertical edge, then they cross.
    return (h.x.min < v.x.min and
            h.x.max > v.x.max and
            v.y.min < h.y.min and
            v.y.max > h.y.max)


def find_crosses(edges):
    """Find all crossing edges"""
    horizontal = [e for e in edges if e.horizontal]
    vertical = [e for e in edges if not e.horizontal]
    return [(h,v) for h in horizontal for v in vertical if edges_cross(h,v)]

