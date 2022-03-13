import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.classes.function import nodes
import random

from scipy import rand 
import util as ut

n,m = 10, 3
alpha, beta = random.random(), random.random()
while alpha==0 or beta==0:
    alpha, beta = random.random(), random.random()
print(alpha, beta)
ri, qi, pi = ut.generer_exemple(n,m, alpha, beta)

zipped_lists = zip(ri, qi, pi)
a = [x+y+z for (x,y,z) in zipped_lists]
C = max(a)
print(C)
di = [C - x for x in qi]
print("di ",di)