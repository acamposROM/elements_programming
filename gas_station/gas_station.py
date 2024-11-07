"""
    We have a vehicle with tank capactiy of U.
    U is the distance the vehcile may travel on a full tank of gas.
    Vertex V is a gas station, where gas can be purchased for c(v), cost of gas per mile
    Gas prices vary at each V.

    The gas station problem: Given a start node s and a target t, how do we go from s
    to t in the cheapest way possible if we start at s with u_s amount of gas?

    Variation: we can only stop to get gas at most N times.
    Variation: Cheapest route that visits a set of p locations in a specified order
"""

import os

import graphviz
import matplotlib

matplotlib.use("module://itermplot")
os.environ["ITERMPLOT_LINES"] = "10"
from io import BytesIO

import matplotlib.pyplot as plt
from PIL import Image


# Nodes will have lists for edges.
# An edge will be a tuple (node, cost to get to node)
class GasStation:
    def __init__(self, name: str, cost: float) -> None:
        self.name = name
        self.cost = cost


class Graph:
    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}
        self.dot = graphviz.Digraph(
            graph_attr={
                "rankdir": "LR",
            }
        )

    def add_node(self, a: GasStation):
        self.nodes[a.name] = a

    def add_edge(self, a: str, b: str, weight: int):
        self.edges[(a, b)] = weight

    def get_node_edges(self, a: str) -> dict:
        return {k: v for k, v in self.edges.items() if k[0] == a}

    def init_graphviz(self) -> None:
        for n in self.nodes.values():
            self.dot.node(n.name, f"{n.name} Cost: {n.cost:.2f}")

        for k, v in self.edges.items():
            a, b = k
            self.dot.edge(str(a), str(b), label=f"{v}")

    def visualize_graph(self) -> None:
        img_data = self.dot.pipe(format="png")
        img = Image.open(BytesIO(img_data))
        img = img.crop(img.getbbox())
        plt.figure(figsize=(16, 6), dpi=300)
        plt.imshow(img)
        plt.axis("off")
        plt.show()

    def __repr__(self) -> str:
        str_builder = []
        # List all nodes
        for n in self.nodes.values():
            str_builder.append(f"Node: {n.name} Cost: {n.cost:.2f}")

        # List all edges
        for k, v in self.edges.items():
            a, b = k
            str_builder.append(f"Edge ({a},{b}) Weight: {v}")

        return "\n".join(str_builder)


a = GasStation("A", 1.00)
b = GasStation("B", 2.00)
G = Graph()
G.add_node(a)
G.add_node(b)
G.add_edge(a.name, b.name, 10)
print(G)

G.init_graphviz()
G.visualize_graph()
