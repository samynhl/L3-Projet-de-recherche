import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

def createIntervals(intervals_list):
    # Returns a list of intervalls that will help build the flow
    intervals_list.sort()
    res = []
    for i in range(len(intervals_list)-1):
        res.append((intervals_list[i], intervals_list[i+1]))
    return res

def generer_exemple(n,m, alpha, beta,verbose=False):
    try:
        somme1, somme2=0,0
        while (somme1==0 or somme2==0):
            alpha, beta = random.random(), random.random()
            pi = [np.random.randint(1,10) for i in range(n)]
            somme1 = (alpha*sum(pi))//m
            somme2 = (beta*sum(pi))//m
        ri = [np.random.randint(0,somme1) for i in range(n)]
        qi = [np.random.randint(0,somme2) for i in range(n)]
        if verbose:
            # Affichage
            print("ri ",ri)
            print("qi ",qi)
            print("pi ",pi)
        return ri, qi, pi
    except Exception:
        print("Une exception a été levée")
        exit

# Initialisations
def init(n=10,m=3):
    tasks = {"ri":[],"di" :[],"pi" :[]}
    alpha, beta =0,0
    while (alpha==0 or beta==0): alpha, beta = random.random(), random.random()
    ri, qi, pi = generer_exemple(n,m, alpha, beta)
    a = [x+y+z for (x,y,z) in zip(ri, qi, pi)]
    C = max(a)
    di = [C - x for x in qi]
    tasks = {"ri":ri,"di" :di,"pi" :pi,"qi":qi}
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
    return G

def générer_instances(n):
    # Génère 100 instances de tests de taille n taches chacun
    # Sauvegarde les résultats dans un fichier de sortie
    def write_example(tasks):
        with open('instances.txt','a') as f:
            f.write(f"{n}\n")
            f.write(f"{tasks['ri']}\n")
            f.write(f"{tasks['pi']}\n")
            f.write(f"{tasks['qi']}\n")
            f.write(f"{tasks['di']}\n")
            f.write(f"---\n")
    m = int(n*0.1) 
    for i in range(100):
        tasks = init(n,m)
        write_example(tasks)
    
def read_example(f):
    def parser(l):
        res = []
        for e in l:
            res.append(int(e))
        return res
    l = ''
    tasks = {'ri':[],'pi':[],'qi':[],'di':[]}
    exemples = []
    n = 0
    while True:
        l = f.readline()
        if l=='---\n': break
        exemples.append(l)
    n = int(exemples[0])
    tasks['ri'] = parser(exemples[1][1:-2].split(','))
    tasks['pi'] = parser(exemples[2][1:-2].split(','))
    tasks['qi'] = parser(exemples[3][1:-2].split(','))
    tasks['di'] = parser(exemples[4][1:-2].split(','))
    return n,tasks