from tkinter import E
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

def generer_exemple(n,m, alpha, beta):
    try:
        pi = [np.random.randint(1,10) for i in range(n)]
        print(pi)
        somme = (alpha*sum(pi))//m
        ri = [np.random.randint(0,somme) for i in range(n)]
        somme = (beta*sum(pi))//m # Probleme si division entière donne 0
        qi = [np.random.randint(0,somme) for i in range(n)]
        # Affichage
        print("ri",ri)
        print("qi",qi)
        print("pi",pi)

        return ri, qi, pi

    except Exception:
        print(somme)
        exit

