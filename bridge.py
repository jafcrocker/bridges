#! /usr/bin/env python

from itertools import chain

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
    def __init__(self, n0, n1):
        self.n0 = n0
        self.n1 = n1
    def __repr__(self):
        return "E:"+str([self.n0,self.n1])

class Puzzle(object):
    def __init__(self, nodes, diamonds):
        self.nodes = make_nodes(nodes)
        self.diamonds = make_diamonds(diamonds)
        self.edges = make_edges(nodes, diamonds)

def make_nodes(nodes):
    return {i:Node(*i) for i in nodes}

def make_diamonds(diamonds):
    return {(x,y):Diamond(x,y,u,r,d,l) for x,y,u,r,d,l in diamonds}

def make_edge(n1, n2):
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

