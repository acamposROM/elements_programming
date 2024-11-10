import os

import graphviz
import matplotlib

matplotlib.use("module://itermplot")
from io import BytesIO

import matplotlib.pyplot as plt
from PIL import Image


class Graph:
    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}
        self.dot = graphviz.Digraph(
            graph_attr={
                "rankdir": "LR",
            }
        )

    def add_node(self, a):
        self.nodes[a.name] = a

    def add_edge(self, a: str, b: str, weight: int):
        self.edges[(a, b)] = weight

    def get_node_edges(self, a: str) -> dict:
        return {k: v for k, v in self.edges.items() if k[0] == a}

    def create_graphviz(self, label="Value") -> None:
        for n in self.nodes.values():
            self.dot.node(n.name, f"{n.name}\n{label}: {n.val:.2f}")

        for node_pair, weight in self.edges.items():
            a, b = node_pair
            self.dot.edge(a, b, label=f"{weight}")

    def visualize_graph(self, matplotlib_backend="") -> None:
        # if not os.getenv("ITERMPLOT_LINES"):
        #     os.environ["ITERMPLOT_LINES"] = "15"
        if matplotlib_backend:
            matplotlib.use(matplotlib_backend)

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
            str_builder.append(f"Node: {n.name} Value: {n.val:.2f}")

        # List all edges
        for k, v in self.edges.items():
            a, b = k
            str_builder.append(f"Edge ({a},{b}) Weight: {v}")

        return "\n".join(str_builder)
