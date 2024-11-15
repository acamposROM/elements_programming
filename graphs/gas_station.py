"""
    We have a vehicle with tank capactiy of U.
    U is the distance the vehcile may travel on a full tank of gas.
    Vertex V is a gas station, where gas can be purchased for c(v), cost of gas per mile
    Gas prices vary at each V.

    The gas station problem: Given a start node s and a target t, how do we go from s
    to t in the cheapest way possible if we start at s with u_s amount of gas?
"""

from graph import Graph
from typing import List, Tuple


# Nodes will have lists for edges.
# An edge will be a tuple (node, val to get to node)
class GasStation:
    def __init__(self, name: str, val: float, curr: bool = False) -> None:
        self.name = name
        self.val = val
        self.curr = curr

    def __repr__(self) -> str:
        return self.name


class GasTank:
    def __init__(self, curr, max) -> None:
        self.curr = curr
        self.max = max


class GasGraph(Graph):
    # def get_node_edges(self, a: GasStation, threshold) -> dict:
    #     return {k: v for k, v in self.edges.items() if k[0] == a.name and v <= threshold}
    def __init__(self) -> None:
        super().__init__()
        self.dp = {}

    def init_dp(self):
        for node in self.nodes.values():
            self.dp[node] = {}

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
The DP will be in the GasGraph. It will consist of dict with nodes as the keys and lists of tuples.
The indices are how much gas to we have when we arrive at that node and the
min cost of that value + the path to take (this might make it extra complicated but i want to have
a path to follow)
what if i made the dict also have an embedded dict for the gas tank values otherwise we just
make Umax * |V| space and it might not even be used. let's use them as needed.
When we calculate once that value, we can store in the list for future use. The s-1 node
will be the one to decide what is the cheapest option by using the available calculation.
"""


def gas_station_min_cost(
    s: GasStation, t: GasStation, G: GasGraph, current_gas: int, max_gas: int
) -> Tuple[int, List[GasStation]]:
    if s == t:
        return (0, [t])

    # DP: Check to see if we have calculated the min cost to get to t from s
    # with the current amount of gas
    if current_gas in G.dp[s]:
        return G.dp[s][current_gas]

    print(f"Current node {s.name} with {current_gas}/{max_gas} gas")

    # First get all node edges to curr node and
    # filter by the GasTank max.
    # if we fill up the gas tank here, we can get to nodes
    # GasTank.max distance away
    edges = G.get_node_edges(s.name)

    # list that contains nodes to check to see if we can reach
    moving_window = [(next_node, dist) for (_, next_node), dist in edges.items()]

    # nodes that we can actually reach that we want to process
    # the min cost values
    station_queue: List[Tuple[GasStation, int]] = []

    while moving_window:
        node, dist = moving_window.pop()
        if dist <= U.max:
            station_queue.append((G.get_node(node), dist))
            next_edges = G.get_node_edges(node)
            # get all the edges from the node in the moving window
            # append all of them into the moving window
            for (_, next_node), next_dist in next_edges:
                moving_window.append((next_node, dist + next_dist))

    print(station_queue)

    # To make this easy, let us assume current_gas = 0. We can do
    # gas tank values later.
    # the min cost for s->t depends on the min cost s+1 -> t
    # plus the cost of gas we fill up at station s, from a range
    # of dist(s, s+1) to U.max. It might be cheaper to fill up
    # to the max amount of gas at s or if we fill up a specific value
    # it might be cheapest. we need to test for all possibilities

    for next_station in station_queue:
        next_node, dist = next_station
        # we need to at least get to this node so we
        # fill up to the dist minus the current amount of gas we have
        for g in range(dist - current_gas, U.max):
            if current_gas not in G.dp[s]:
                G.dp[s][current_gas] = (float("inf"), [])
            min_cost_next_node_result = gas_station_min_cost(
                next_node, t, G, g - dist, max_gas
            )
            cost_to_get_to_next_node = g * s.val + min_cost_next_node_result[0]
            # If the costs are equal, I think we defer to the node that's furthest away
            # but that means we probably need to figure out distances of neighbors of nodes or store
            # the distances this node is away compared to the other ones in the station_queue or something ugh
            if cost_to_get_to_next_node < G.dp[s][current_gas][0]:
                G.dp[s][current_gas] = (
                    cost_to_get_to_next_node,
                    [s] + min_cost_next_node_result[1],
                )

    return G.dp[s][current_gas]


a = GasStation("A", 1.00, curr=True)
b = GasStation("B", 2.00)
G = GasGraph()
G.add_node(a)
G.add_node(b)
G.add_edge(a.name, b.name, 10)
print(G)
U = GasTank(curr=0, max=20)

G.init_dp()
# This should be 10
print(gas_station_min_cost(a, b, G, U.curr, U.max))

# NEXT TEST CASE A:0.5 10 B:2 5 C:1 15/20 Gas at A. We can just get to C no cost
# do we always just fill up at the current gas station if
# the gas is cheaper here than the next node?
# NEXT TEST CASE A:0.5 10 B:2 5 C:1 14/20 Gas at A
# we should fill up 1 gallon at A because it's the cheapest

# G.create_graphviz(gas_tank=U)
# G.visualize_graph()
