import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math
import time
from networkx.classes.function import nodes
from networkx.algorithms.flow import build_residual_network
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.flow import edmonds_karp
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow import preflow_push
from networkx.algorithms.flow import dinitz
from networkx.algorithms.flow import boykov_kolmogorov
from networkx.algorithms.flow import gomory_hu_tree

import util as ut
import random

algo_names = ['edmonds_karp','shortest_augmenting_path','preflow_push','dinitz','boykov_kolmogorov']
ALGORITHMES = [edmonds_karp,shortest_augmenting_path,preflow_push,dinitz,boykov_kolmogorov]

# Initialisations
def init(n=10,m=3):
    tasks = {"ri":[],"di" :[],"pi" :[]}
    alpha, beta =0,0
    while (alpha==0 or beta==0): alpha, beta = random.random(), random.random()
    ri, qi, pi = ut.generer_exemple(n,m, alpha, beta)
    a = [x+y+z for (x,y,z) in zip(ri, qi, pi)]
    C = max(a)
    di = [C - x for x in qi]
    tasks = {"ri":ri,"di" :di,"pi" :pi}
    return tasks

# Affichage du graphe construit
def affichage(A,r=0):
    weights,caps = nx.get_edge_attributes(A, 'weight'),nx.get_edge_attributes(A, 'capacity')
    for u,v in A.edges:
        if r:
            print(f'({u}, {v}): {caps[(u, v)]}')
        else: 
            print(f'({u}, {v}): {weights[u,v]}/{caps[(u, v)]}')
    print("---")

def plot_graph(G):
    pos=nx.spring_layout(G)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def jackson_heur(G,tasks):
    # Jackson heuristique 
    dico = {}
    for n in G.nodes: dico[n] = list(G.successors(n))
    sorted_ddl = np.argsort(tasks["di"])
    for i in sorted_ddl:
        # Lire les poids et capacités des arcs
        weights,caps = nx.get_edge_attributes(G, 'weight'),nx.get_edge_attributes(G, 'capacity')
        pi = tasks['pi'][i]
        its = dico[str(i+1)]
        itmax,vmax= '',0
        # Selectionner l'intervalle le plus long
        for it in its:
            v = caps[str(i+1), it]-weights[str(i+1), it]
            if v>vmax: vmax,itmax = v,it
        v = min(vmax,pi,caps['s', str(i+1)]-weights['s', str(i+1)],caps[itmax, 'p']-weights[itmax, 'p'])
        if v!=0:
            w1,w2,w3 = weights['s', str(i+1)]+v,weights[str(i+1), itmax]+v,weights[itmax, 'p']+v
            cp1, cp2, cp3 = caps['s', str(i+1)],caps[str(i+1), itmax],caps[itmax, 'p']
            G.add_edge('s', str(i+1), weight=w1,capacity=cp1)
            G.add_edge(str(i+1), itmax, weight=w2,capacity=cp2)
            G.add_edge(itmax, 'p', weight=w3,capacity=cp3)

def main():
    n,m=20,5
    nb_test = 1000
    for algo in ALGORITHMES:
        nb_oui, nb_non = 0,0
        duree = 0
        for i in range(nb_test):
            tasks = init(n,m)
            intervals__values = list(dict.fromkeys(tasks["ri"] + tasks["di"]))
            intervals_list = ut.createIntervals(intervals__values)
            nb_tasks = len(tasks["ri"])

            # Construction du graphe
            G = nx.DiGraph()
            for t in range(nb_tasks):
                G.add_edge('s', str(t+1), weight=0,capacity=tasks["pi"][t])
            for t in range(nb_tasks):
                for k in range(len(intervals_list)):
                    it = intervals_list[k]
                    long_int = it[1]-it[0]
                    if (tasks["ri"][t]<=it[0] and tasks["di"][t]>=it[1]):
                        G.add_edge(str(t+1), "I"+str(k+1), weight=0,capacity=long_int)
            for k in range(len(intervals_list)):
                it = intervals_list[k]
                long_int = it[1]-it[0]
                G.add_edge("I"+str(k+1), "p",weight=0, capacity=m*long_int)
            
            # affichage(G)
            # Jackson heuristique
            
            #jackson_heur(G,tasks)
            #weights,caps = nx.get_edge_attributes(G, 'weight'),nx.get_edge_attributes(G, 'capacity')
            
            R = build_residual_network(G, 'capacity')
            #affichage(G)
            tic = time.time()
            # Résolution du flot maximum
            flow_value, flows = nx.maximum_flow(G, 's', 'p',flow_func=algo,residual=R)
            duree_total = sum(tasks["pi"])
            '''
            # Affichage du flot après résolution du flot maximum
            caps = nx.get_edge_attributes(G, 'capacity')
            for u in nx.topological_sort(G):
                for v, flow in sorted(flows[u].items()):
                    print(f'({u}, {v}): {flow}/{caps[(u, v)]}')
            '''
            check = (duree_total<=flow_value)
            '''
            print("-------------------------------------------------------------------------")
            print(f'maximum flow: {flow_value}')
            print("la réponse au problème de décision : {}".format('Oui' if check else 'Non'))
            '''
            nb_oui+=1 if check else 0
            nb_non+=1 if not check else 0

            duree += time.time()-tic

        print("Pourcentage de réponses oui : ",round(nb_oui/nb_test,2))
        print("Pourcentage de réponses non : ",round(nb_non/nb_test,2))
        print(f'Algo : {str(algo)} - Exécuté en {round(duree,2)} ')
    # Affichage graphique du graphe obtenu
    # plot_graph(G)
main()