import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.classes.function import nodes

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
import time

def main():
    f = open("opt/r7.txt","a")
    # Initialisations
    n = 1000        # Nombre de taches
    m = int(n*0.1)   # Nombre de machines
    tasks = ut.init(n,m)
    C = max([x+y+z for (x,y,z) in zip(tasks["ri"], tasks["qi"], tasks["pi"])])
    intervals__values = list(dict.fromkeys(tasks["ri"] + tasks["di"]))
    intervals_list = ut.createIntervals(intervals__values)

    # Problème d'optimisation
    # Réflexion sur la manière de générer les bornes
    binf = max(int(sum(tasks["pi"])/m+1),max([x+y+z for (x,y,z) in zip(tasks["qi"], tasks["pi"], tasks["ri"])]))
    bsup = sum(tasks["pi"])
    C = int((binf+bsup)//2)

    nb_iterations = 0
    tic = time.time()
    while(True):
        nb_iterations+=1
        print("binf : ", binf)
        print("bsup : ", bsup)
        print("C : ", C)
        nodes_list = []
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

        # Jackson heuristique 
        # G = jackson_heur(G,tasks)
        # Résolution du flot maximum
        flow_value, flows = nx.maximum_flow(G, 's', 'p',flow_func=shortest_augmenting_path)
        duree_total = sum(tasks["pi"])
        '''
        # Affichage du flot après résolution du flot maximum
        caps = nx.get_edge_attributes(G, 'capacity')
        for u in nx.topological_sort(G):
            for v, flow in sorted(flows[u].items()):
                print(f'({u}, {v}): {flow}/{caps[(u, v)]}')
        '''
        check = (duree_total<=flow_value)
        print(f'maximum flow: {flow_value}')
        print("la réponse au problème de décision : {}".format('Oui' if check else 'Non'))
        print("-------------------------------------------------------------------------")

        # Sauvegarde du résultat dans le fichier de sortie
        f.write("C={}, n={}, m={}\n".format(C,n,m))
        f.write("ri={}\n".format(tasks["ri"]))
        f.write("di={}\n".format(tasks["di"]))
        f.write("qi={}\n".format(tasks["qi"]))
        f.write("pi={}\n".format(tasks["pi"]))
        f.write("Probleme de decision : {}\n".format('Oui' if check else 'Non'))
        f.write("-----------------------------------------------------------------------------\n")
        
        if check:
            bsup = C
            Copt = C
        else: binf = C
        # Condition d'arret
        if bsup-binf<2: break

        C = int((binf+bsup)//2)

        di = [C - x for x in tasks["qi"]]
        tasks["di"] = di
    print(f'n= {n}, m= {m}')
    print("la valeur de C optimal: ", Copt)
    print("Trouvé en {} itérations".format(nb_iterations))
    print("Temps d'exécution : ",round(time.time()-tic,2))

    # Sauvegarde du résultat dans le fichier de sortie
    f.write("C={}, n={}, m={}\n".format(C,n,m))
    f.write("ri={}\n".format(tasks["ri"]))
    f.write("di={}\n".format(tasks["di"]))
    f.write("qi={}\n".format(tasks["qi"]))
    f.write("pi={}\n".format(tasks["pi"]))
    f.write("Probleme de decision : {}\n".format('Oui' if check else 'Non'))
    f.write("-----------------------------------------------------------------------------\n")
    f.write("-----------------------------------------------------------------------------\n")
    f.write(f'n= {n}, m= {m}\n')
    f.write("la valeur de C optimal: {}\n".format(Copt))
    f.write("Trouve en {} iterations\n".format(nb_iterations))
    f.write("Temps d'execution : {}\n".format(round(time.time()-tic,2)))

    f.close()

main()