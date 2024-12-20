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
    # Base Case
    if s == t:
        return CostToTakePath(0.00, [])

    # DP: Check to see if we have calculated the min cost to get to t from s
    # with the current amount of gas otherwise init the dict
    if current_gas in G.dp[s]:
        return G.dp[s][current_gas]
    else:
        G.dp[s][current_gas] = CostToTakePath(float("inf"), [])

    # First, get all node edges to curr node
    edges = G.get_node_edges(s.name)
    moving_window = [(next_node, dist) for (_, next_node), dist in edges.items()]

    # Initializing dict of valid stations we can reach.
    # Making this a dict to access distances away from s
    # for when two nodes have the same min cost in the
    # recursive DP loop later on
    reachable_stations_dict: Dict[GasStation, int] = {}

    while moving_window:
        node, dist = moving_window.pop()
        # if dist is greater than max gas of car, we cannot reach the node
        if dist <= max_gas:
            reachable_stations_dict[G.get_node(node)] = dist
            next_edges = G.get_node_edges(node)
            # get all the edges from the child node in the moving window
            # append all of them into the moving window
            for (_, next_node), next_dist in next_edges.items():
                moving_window.append((next_node, dist + next_dist))

    # the min cost for s-> depends on the min cost s+1 -> t
    # plus the cost of gas we filled up at s. The range of
    # potential gas values g we can fill up will depend on
    # how much gas we currently have. We have to compute all
    # of them because we do not know if further down the path
    # it would be cheaper to fill up a constant amount at S because
    # it will minimize costs at s_n-1.
    for next_station in reachable_stations_dict.items():
        next_node, dist = next_station
        # The range of gas values will either be 0 if current gas is greater
        # than dist, or dist - current gas, because that is how much gas we
        # need to even get to next_node
        start_gas_val = dist - current_gas if current_gas < dist else 0
        for g in range(start_gas_val, (max_gas - current_gas + 1)):
            min_cost_next_node_result = gas_station_min_cost(
                next_node, t, G, current_gas + g - dist, max_gas
            )
            total_cost_of_path = g * s.val + min_cost_next_node_result.cost
            # If the costs are equal, choose the one furthest away.
            if total_cost_of_path == G.dp[s][current_gas].cost:
                cached_path_node_head = G.dp[s][current_gas].path[0]
                dist_to_cached_node = reachable_stations_dict[cached_path_node_head]
                if dist > dist_to_cached_node:
                    G.dp[s][current_gas] = CostToTakePath(
                        total_cost_of_path,
                        [next_node] + min_cost_next_node_result.path,
                    )
            elif total_cost_of_path < G.dp[s][current_gas].cost:
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
