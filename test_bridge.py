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

class TestEdgesCross(unittest.TestCase):
    def test_crosses(self):
        s = """\
         o
        o o
         o
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertTrue(bridge.edges_cross(edges[1], edges[0]))
    def test_contiguous1(self):
        s = """\
        oo
         o
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_contiguous2(self):
        s = """\
         o
        oo
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_contiguous3(self):
        s = """\
        oo
        o
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_contiguous4(self):
        s = """\
        oo
        o
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_disjoint1(self):
        s = """\
        oo
          o
          o
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_disjoint2(self):
        s = """\
          o
          o
        oo
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_disjoint3(self):
        s = """\
         oo
        o
        o
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
    def test_disjoint4(self):
        s = """\
        o
        o
         oo
        """
        node_data = bridge.load_string(dedent(s))
        nodes = bridge.make_nodes(node_data)
        edges = bridge.make_edges(nodes, [])
        self.assertFalse(bridge.edges_cross(edges[1], edges[0]))
