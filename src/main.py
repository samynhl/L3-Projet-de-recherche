import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.classes.function import nodes
import util as ut



# Initialisations
m = 2
tasks = {"ri": [0, 0, 1],
         "di": [1, 4, 4],
         "pi": [1, 2, 3]}

m = 3
tasks = {"ri":[0,0,1,2],
        "di" :[1,3,5,6],
        "pi" :[1,2,3,3]}

tasks = {"ri":[],
        "di" :[],
        "pi" :[]}
n,m = 10, 3
alpha, beta = np.random.rand(), np.random.rand()
ri, qi, pi = ut.generer_exemple(n,m, alpha, beta)

zipped_lists = zip(ri, qi, pi)
a = [x+y+z for (x,y,z) in zipped_lists]
C = max(a)

def main():
    nodes_list = []
    intervals__values = list(dict.fromkeys(tasks["ri"] + tasks["di"]))
    intervals_list = ut.createIntervals(intervals__values)
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