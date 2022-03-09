import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.classes.function import nodes


def generer_exemple(n,m, alpha, beta):
    pi = [np.random.randint(1,10) for i in range(n)]
    somme = alpha*sum(pi)//m
    print(somme)
    ri = [np.random.randint(0,somme) for i in range(n)]
    somme = beta*sum(pi)//m
    qi = [np.random.randint(0,somme) for i in range(n)]

    # Affichage
    print("pi",pi)
    print("ri",ri)
    print("qi",qi)
    
    return pi, ri, qi



# 
n,m = 10, 3
alpha, beta = np.random.rand(), np.random.rand()
generer_exemple(n,m, alpha, beta)