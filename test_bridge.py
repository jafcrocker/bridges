import unittest
import bridge
from textwrap import dedent


class TestLoadString(unittest.TestCase):
    def test_oneline(self):
        s = "o o  o"
        expected = [(0,0), (2,0), (5,0)]
        self.assertEqual(bridge.load_string(s), expected)
    def test_multiline(self):
        s = dedent("""\
            o o o
             o o
              o
            """)
        expected = [(0,0), (2,0), (4,0), (1,1), (3,1), (2,2)]
        self.assertEqual(bridge.load_string(s), expected)


class TestMakeEdges(unittest.TestCase):
    def test_nodes(self):
        node_data = [(0,0), (2,0), (3,0), (0,1), (3,1), (2,2)]
        expected = {(0,0): ((0,1), (2,0)),
                    (2,0): ((0,0), (2,2), (3,0)),
                    (3,0): ((2,0), (3,1)),
                    (0,1): ((0,0), (3,1)),
                    (3,1): ((0,1), (3,0)),
                    (2,2): ((2,0),)}
        nodes = bridge.make_nodes(node_data)
        e = bridge.make_edges(nodes, [])
        self.assertEqual(len(e), 6)
        for k, v in expected.iteritems():
            n = nodes[k]
            self.assertEqual(len(n.edges),len(v))


    def test_diamonds(self):
        node_data = [(0,0), (2,0), (3,0), (0,1), (3,1), (2,2)]
        diamond_data = [(1,0,0,0,0,0),(2,1,0,0,0,0)]
        expected = {(0,0): ((0,1), ),
                    (2,0): ((3,0), ),
                    (3,0): ((2,0), (3,1)),
                    (0,1): ((0,0), ),
                    (3,1): ((0,1), ),
                    (2,2): ()}
        nodes = bridge.make_nodes(node_data)
        diamonds = bridge.make_diamonds(diamond_data)
        e = bridge.make_edges(nodes, diamond_data)
        self.assertEqual(len(e), 3)
        for k, v in expected.iteritems():
            n = nodes[k]
            self.assertEqual(len(n.edges),len(v))

