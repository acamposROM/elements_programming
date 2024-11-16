"""
    We have a vehicle with tank capactiy of U.
    U is the distance the vehcile may travel on a full tank of gas.
    Vertex V is a gas station, where gas can be purchased for c(v), cost of gas per mile
    Gas prices vary at each V.

    The gas station problem: Given a start node s and a target t, how do we go from s
    to t in the cheapest way possible if we start at s with u_s amount of gas?
"""

from typing import Dict, List, NamedTuple, Tuple

from graph import Graph


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
        self.dp: Dict[GasStation, Dict[int, CostToTakePath]] = {}

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


class CostToTakePath(NamedTuple):
    cost: float
    path: List[GasStation]

    def __repr__(self) -> str:
        return f"Cost: {self.cost:.2f} Path:{self.path}"


"""
Find the min cost to get from S to T in Graph G, with gas tank U
The DP will be in the GasGraph. It will consist of a nested dict with nodes as
the first level keys, and the second layer keys being possible gas tank values
at that node
"""


def gas_station_min_cost(
    s: GasStation, t: GasStation, G: GasGraph, current_gas: int, max_gas: int
) -> CostToTakePath:
    if s == t:
        return CostToTakePath(0.00, [])

    # DP: Check to see if we have calculated the min cost to get to t from s
    # with the current amount of gas otherwise init the dict
    if current_gas in G.dp[s]:
        return G.dp[s][current_gas]
    else:
        G.dp[s][current_gas] = CostToTakePath(float("inf"), [])

    # First get all node edges to curr node and
    # filter by the GasTank max.
    # if we fill up the gas tank here, we can get to nodes
    # GasTank.max distance away
    edges = G.get_node_edges(s.name)
    moving_window = [(next_node, dist) for (_, next_node), dist in edges.items()]

    # Initializing dict of valid stations we can vist.
    # Making this a dict to access distances for an edge case.
    station_dict: Dict[GasStation, int] = {}

    # Process all nodes in the moving window to submit them into the station_queue
    while moving_window:
        node, dist = moving_window.pop()
        if dist <= max_gas:
            station_dict[G.get_node(node)] = dist
            next_edges = G.get_node_edges(node)
            # get all the edges from the node in the moving window
            # append all of them into the moving window
            for (_, next_node), next_dist in next_edges.items():
                moving_window.append((next_node, dist + next_dist))

    # To make this easy, let us assume current_gas = 0. We can do
    # gas tank values later.
    # the min cost for s->t depends on the min cost s+1 -> t
    # plus the cost of gas we fill up at station s, from a range
    # of dist(s, s+1) to U.max. It might be cheaper to fill up
    # to the max amount of gas at s or if we fill up a specific value
    # it might be cheapest. we need to test for all possibilities

    for next_station in station_dict.items():
        next_node, dist = next_station

        # we need to at least get to this node so we
        # fill up to the dist minus the current amount of gas we have
        for g in range(0, (max_gas - current_gas + 1)):
            # TODO: how do i build my for loop to just find the ranges for this condition
            if g + current_gas < dist:
                continue
            min_cost_next_node_result = gas_station_min_cost(
                next_node, t, G, current_gas + g - dist, max_gas
            )
            total_cost_of_path = g * s.val + min_cost_next_node_result.cost
            # If the costs are equal, I think we defer to the node that's furthest away
            # but that means we probably need to figure out distances of neighbors of nodes or store
            # the distances this node is away compared to the other ones in the station_queue or something ugh
            if total_cost_of_path < G.dp[s][current_gas].cost:
                G.dp[s][current_gas] = CostToTakePath(
                    total_cost_of_path,
                    [next_node] + min_cost_next_node_result.path,
                )
            elif total_cost_of_path == G.dp[s][current_gas].cost:
                # Grab the next node in the previously saved path
                # print(f'current cost saved {G.dp[s][current_gas].cost}')
                # print(f'total cost of new path: {total_cost_of_path}')
                # print(G.dp[s][current_gas].path)
                saved_path_node_head = G.dp[s][current_gas].path[0]
                dist_to_next_node_head = station_dict[saved_path_node_head]
                # if the distance of thi
                if dist > dist_to_next_node_head:
                    G.dp[s][current_gas] = CostToTakePath(
                        total_cost_of_path,
                        [next_node] + min_cost_next_node_result.path,
                    )

    return G.dp[s][current_gas]


a = GasStation("A", 1.00, curr=True)
b = GasStation("B", 2.00)
G = GasGraph()
G.add_node(a)
G.add_node(b)
G.add_edge(a.name, b.name, 10)
U = GasTank(curr=0, max=20)

G.init_dp()
# This should be 10
print(gas_station_min_cost(a, b, G, U.curr, U.max))

c = GasStation("C", 1.00)
d = GasStation("D", 2.00)
e = GasStation("E", 0.01)
f = GasStation("F", 0.50)
G_2 = GasGraph()
G_2.add_node(c)
G_2.add_node(d)
G_2.add_node(e)
G_2.add_node(f)

G_2.add_edge(c.name, d.name, 10)
G_2.add_edge(d.name, e.name, 10)
G_2.add_edge(e.name, f.name, 20)
# G_2.create_graphviz(gas_tank=U)
# G_2.visualize_graph()

G_2.init_dp()
print(gas_station_min_cost(c, f, G_2, U.curr, U.max))

# NEXT TEST CASE A:0.5 10 B:2 5 C:1 14/20 Gas at A
# we should fill up 1 gallon at A because it's the cheapest
G_3 = GasGraph()
g = GasStation("G", 0.5)
i = GasStation("I", 2.0)
j = GasStation("J", 1.0)
G_3.add_node(g)
G_3.add_node(i)
G_3.add_node(j)
G_3.add_edge(g.name, i.name, 10)
G_3.add_edge(i.name, j.name, 5)

G_3.init_dp()
print(gas_station_min_cost(g, j, G_3, 14, 20))

# NEXT TEST CASE A:0.5 10 B:2 5 C:1 15/20 Gas at A. We can just get to C no cost
