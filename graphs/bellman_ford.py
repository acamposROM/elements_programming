"""
This file implements the bellman ford algo to find the shortest path from a single source
"""

import graphviz

from graph import Graph


class Vertex:
    def __init__(self, name, val) -> None:
        self.name = name
        self.val = val
        self.prev = None

    def __repr__(self) -> str:
        return f"Node: {self.name}, Value: {self.val}"


class BFGraph(Graph):
    def visualize_graph(self, matplotlib_backend="") -> None:
        return super().visualize_graph(matplotlib_backend)

    def update_graphviz_edge(self, a: Vertex, b: Vertex, color=""):
        weight = self.edges[(a.name, b.name)]
        self.dot.edge(a.name, b.name, label=f"{weight}", color=color)

    def create_graphviz(self, label="Value") -> None:
        self.dot = graphviz.Digraph(
            graph_attr={
                "rankdir": "LR",
            }
        )

        for n in self.nodes.values():
            self.dot.node(n.name, f"{n.name}\n{label}: {n.val:.2f}")

        for node_pair, weight in self.edges.items():
            a, b = node_pair
            a_node = self.nodes[a]
            b_node = self.nodes[b]
            if b_node.prev == a_node:
                self.dot.edge(a, b, label=f"{weight}", color="red")
            else:
                self.dot.edge(a, b, label=f"{weight}")


def bellman_ford(G: BFGraph, root: Vertex):
    root.val = 0
    for _ in range(len(G.nodes.keys())):
        for e, w in G.edges.items():
            a_name, b_name = e
            a = G.nodes[a_name]
            b = G.nodes[b_name]
            # Relaxation part for node values p649
            if b.val > a.val + w:
                b.val = a.val + w
                b.prev = a
        G.create_graphviz()
        G.visualize_graph()

    # Checking to see if there are negative weight cycles
    for e, w in G.edges.items():
        a_name, b_name = e
        a = G.nodes[a_name]
        b = G.nodes[b_name]
        # if we find that even after doing
        # |G.V| - 1 relaxation steps there are still
        # weights we can update, we are in a cycle
        if b.val > a.val + w:
            return False

    return True


# Setting up example from pg 652 of CLSR
s = Vertex("s", float("inf"))
t = Vertex("t", float("inf"))
y = Vertex("y", float("inf"))
x = Vertex("x", float("inf"))
z = Vertex("z", float("inf"))

vertices = [s, t, y, x, z]
edges = [
    ("t", "x", 5),
    ("t", "y", 8),
    ("t", "z", -4),
    ("x", "t", -2),
    ("y", "x", -3),
    ("z", "x", 7),
    ("z", "s", 2),
    ("s", "t", 6),
    ("s", "y", 7),
]

G = BFGraph()
for v in vertices:
    G.add_node(v)

for e in edges:
    G.add_edge(*e)

G.create_graphviz()
G.visualize_graph()

bellman_ford(G, s)
