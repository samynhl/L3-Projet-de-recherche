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

# Générer exemples
# for n in range(100, 2000, 200):
#        ut.générer_instances(n)
# return
def main():
    exec_time = []
    valeurs_n = []
    nb_test = 100
    f1 = open('instances.txt','r')
    f2 = open('di_h.txt','a')
    for n in range(100, 800, 200):
        nb_oui, nb_non = 0,0
        duree = 0
        for i in range(nb_test):
            n,tasks = ut.read_example(f1)
            m = int(n*0.1)
            intervals__values = list(dict.fromkeys(tasks["ri"] + tasks["di"]))
            intervals_list = ut.createIntervals(intervals__values)

            # Construction du graphe
            G = nx.DiGraph()
            for t in range(n):
                G.add_edge('s', str(t+1), weight=0,capacity=tasks["pi"][t])
            for t in range(n):
                for k in range(len(intervals_list)):
                    it = intervals_list[k]
                    long_int = it[1]-it[0]
                    if (tasks["ri"][t]<=it[0] and tasks["di"][t]>=it[1]):
                        G.add_edge(str(t+1), "I"+str(k+1), weight=0,capacity=long_int)
            for k in range(len(intervals_list)):
                it = intervals_list[k]
                long_int = it[1]-it[0]
                G.add_edge("I"+str(k+1), "p",weight=0, capacity=m*long_int)
            
            # ut.affichage(G)
            # Jackson heuristique
            
            G = ut.jackson_heur(G,tasks)
            weights,caps = nx.get_edge_attributes(G, 'weight'),nx.get_edge_attributes(G, 'capacity')
            
            R = build_residual_network(G, 'capacity')
            #affichage(G)
            tic = time.time()
            # Résolution du flot maximum
            flow_value, flows = nx.maximum_flow(G, 's', 'p',flow_func=dinitz,residual=R)
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
        valeurs_n.append(n)
        exec_time.append(duree)
        print(n,m)
        print("Taux de réponses oui : ",round(nb_oui/nb_test,2))
        print("Taux de réponses non : ",round(nb_non/nb_test,2))
        print(f'Algo : dinitz - Exécuté en {round(duree,2)} ')
        print("---")

        f2.write(f'n= {n}, m= {m}\n')
        f2.write(f'Taux de reponses oui : {round(nb_oui/nb_test,2)}\n')
        f2.write(f'Taux de reponses non : {round(nb_non/nb_test,2)}\n')
        f2.write(f'Algo : dinitz - Execute en {round(duree,2)}\n')
        f2.write("---\n")
    
    f2.write(f'{valeurs_n}\n')
    f2.write(f'{exec_time}\n')

    f1.close()
    f2.close()

    plt.plot(valeurs_n,exec_time)
    plt.xlabel('Nombre de taches n')
    plt.ylabel("Temps d'exécution")
    plt.title('Algorithme de dinitz avec heuristique de jackson') 
    #plt.show()
    plt.savefig('di_h.png')
    # Affichage graphique du graphe obtenu
    # plot_graph(G)

main()