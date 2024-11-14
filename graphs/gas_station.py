"""
    We have a vehicle with tank capactiy of U.
    U is the distance the vehcile may travel on a full tank of gas.
    Vertex V is a gas station, where gas can be purchased for c(v), cost of gas per mile
    Gas prices vary at each V.

    The gas station problem: Given a start node s and a target t, how do we go from s
    to t in the cheapest way possible if we start at s with u_s amount of gas?
"""

from graph import Graph


# Nodes will have lists for edges.
# An edge will be a tuple (node, val to get to node)
class GasStation:
    def __init__(self, name: str, val: float, curr: bool = False) -> None:
        self.name = name
        self.val = val
        self.curr = curr


class GasTank:
    def __init__(self, curr, max) -> None:
        self.curr = curr
        self.max = max


class GasGraph(Graph):
    # def get_node_edges(self, a: GasStation, threshold) -> dict:
    #     return {k: v for k, v in self.edges.items() if k[0] == a.name and v <= threshold}

    def create_graphviz(self, label="Value", gas_tank: GasTank = GasTank(0, 0)) -> None:
        for n in self.nodes.values():
            if n.curr:
                self.dot.node(
                    n.name,
                    f"{n.name}\n{label}: {n.val:.2f}\nGas Tank: {gas_tank.curr}/{gas_tank.max}",
                    style="filled",
                    fillcolor="lightgreen",
                )
            else:
                self.dot.node(n.name, f"{n.name}\n{label}: {n.val:.2f}")

        for node_pair, weight in self.edges.items():
            a, b = node_pair
            self.dot.edge(a, b, label=f"{weight}")


"""
Find the min cost to get from S to T in Graph G, with gas tank U
"""


def gas_station_min_cost(s, t, G: GasGraph, U: GasTank):
    if s == t:
        return 0

    print(f"Starting at node {s.name} with {U.curr}/{U.max} gas")
    # First get all node edges to curr node and
    # filter by the GasTank max.
    # if we fill up the gas tank here, we can get to nodes
    # GasTank.max distance away

    edges = G.get_node_edges(s.name)

    # list that contains nodes to check to see if we can reach
    moving_window = [(next_node, dist) for (_, next_node), dist in edges.items()]

    # nodes that we can actually reach that we want to process
    # the min cost values
    dp_queue = []
    while moving_window:
        node, dist = moving_window.pop()
        if dist <= U.max:
            dp_queue.append((G.get_node(node), dist))
            next_edges = G.get_node_edges(node)
            # get all the edges from the node in the moving window
            # append all of them into the moving window
            for (_, next_node), next_dist in next_edges:
                moving_window.append((next_node, dist + next_dist))

    print(dp_queue)

    # the min cost for s->t depends on which
    # node in the queue gives the min cost and the range of
    # all possible gas filling values g from 0 <= g <= Umax - Ucurr
    # for next_node, dist in queue:
    #   for g in range(0, U.max - U.curr + 1):
    #       cost = min(cost, min_cost(next_node, t, U_curr + g - dist))
    #              + g * curr_node.val ( the amount of gallons * cost at this node)

    # the DP here is storing the smaller graphs min cost so that we do
    # not have to recalculate all the moving window AND min cost stuff
    for g in range(0, U.max - U.curr + 1):
        print(g)
    return 0


a = GasStation("A", 1.00, curr=True)
b = GasStation("B", 2.00)
G = GasGraph()
G.add_node(a)
G.add_node(b)
G.add_edge(a.name, b.name, 10)
print(G)
U = GasTank(10, 20)

gas_station_min_cost(a, b, G, U)

# NEXT TEST CASE A:0.5 10 B:2 5 C:1 15/20 Gas at A. We can just get to C no cost
# do we always just fill up at the current gas station if
# the gas is cheaper here than the next node?
# NEXT TEST CASE A:0.5 10 B:2 5 C:1 14/20 Gas at A
# we should fill up 1 gallon at A because it's the cheapest

# G.create_graphviz(gas_tank=U)
# G.visualize_graph()
