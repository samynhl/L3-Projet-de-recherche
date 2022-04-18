import numpy as np
import random

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

