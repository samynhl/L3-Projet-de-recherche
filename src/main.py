import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.classes.function import nodes


def createIntervals(intervals_list):
    # Returns a list of intervalls that will help build the flow

    # printing original list
    intervals_list.sort()
    print("The original list : " + str(intervals_list))

    res = []
    for i in range(len(intervals_list)-1):
        res.append((intervals_list[i], intervals_list[i+1]))
    # printing result
    print("Resulting intervals : " + str(res))
    return res

# Initialisations
m = 2
tasks = {"ri": [0, 0, 1],
         "di": [1, 4, 4],
         "pi": [1, 2, 3]}

m = 3
tasks = {"ri":[0,0,1,2],
        "di" :[1,3,5,6],
        "pi" :[1,2,3,3]}

m = 3
tasks = {"ri":[0,0,1],
        "di" :[1,3,6],
        "pi" :[1,2,3]}


def main():
    nodes_list = []
    intervals__values = list(dict.fromkeys(tasks["ri"] + tasks["di"]))
    intervals_list = createIntervals(intervals__values)
    nb_tasks = len(tasks["ri"])
    for t in range(nb_tasks):
        nodes_list.append((('s', str(t+1), dict(capacity=tasks["pi"][t]))))
    for t in range(nb_tasks):
        for k in range(len(intervals_list)):
            it = intervals_list[k]
            long_int = it[1]-it[0]
            if (tasks["ri"][t]<=it[0] and tasks["di"][t]>=it[1]):
                nodes_list.append(((str(t+1), "I"+str(k+1), dict(capacity=long_int))))
    for k in range(len(intervals_list)):
        it = intervals_list[k]
        long_int = it[1]-it[0]
        nodes_list.append((("I"+str(k+1), "p", dict(capacity=m*long_int))))
    for el in nodes_list:
        print(el)

    G = nx.DiGraph()
    G.add_edges_from(nodes_list)
    duree_total = sum(tasks["pi"])
    flow_value, flows = nx.maximum_flow(G, 's', 'p')
    print(f'maximum flow: {flow_value}')
    nx.draw(G, with_labels=True, font_weight='bold')
    caps = nx.get_edge_attributes(G, 'capacity')
    for u in nx.topological_sort(G):
        for v, flow in sorted(flows[u].items()):
            print(f'({u}, {v}): {flow}/{caps[(u, v)]}')

    check = (duree_total<=flow_value)
    print("-------------------------------------------------------------------------")
    print("la réponse au problème de décision : {}".format('Oui' if check else 'Non'))

main()