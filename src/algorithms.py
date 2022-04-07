import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.classes.function import nodes
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.flow import edmonds_karp
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow import preflow_push
from networkx.algorithms.flow import dinitz
from networkx.algorithms.flow import boykov_kolmogorov
from networkx.algorithms.flow import gomory_hu_tree

import util as ut
import random

ALGORITHMES = ['maximum_flow','edmonds_karp','shortest_augmenting_path',
             'preflow_push','dinitz','boykov_kolmogorov','gomory_hu_tree']

# Initialisations
tasks = {"ri":[],"di" :[],"pi" :[]}
n,m = 10, 3
alpha, beta =0,0
while (alpha==0 or beta==0): alpha, beta = random.random(), random.random()
ri, qi, pi = ut.generer_exemple(n,m, alpha, beta)
a = [2*x+2*y+2*z for (x,y,z) in zip(ri, qi, pi)]
C = max(a)
di = [C - x for x in qi]
print("di ",di)
tasks = {"ri":ri,"di" :di,"pi" :pi}

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
        nodes_list.append((("I"+str(k+1), "p", dict(weight=1,capacity=m*long_int))))
    for el in nodes_list:
        print(el)
    
    G = nx.DiGraph()
    G.add_edges_from(nodes_list)
    G.add_edge("s", "1", weight=1)
    duree_total = sum(tasks["pi"])
    flow_value, flows = nx.maximum_flow(G, 's', 'p',flow_func=edmonds_karp)
    for k,v in flows.items():
        print(k,v)
    print(f'maximum flow: {flow_value}')
    nx.draw(G, with_labels=True, font_weight='bold')
    caps = nx.get_edge_attributes(G, 'capacity')
    for u in nx.topological_sort(G):
        for v, flow in sorted(flows[u].items()):
            print(f'({u}, {v}): {flow}/{caps[(u, v)]}')

    check = (duree_total<=flow_value)
    print("-------------------------------------------------------------------------")
    print("C: ", C)
    print(f'maximum flow: {flow_value}')
    print("la réponse au problème de décision : {}".format('Oui' if check else 'Non'))

main()