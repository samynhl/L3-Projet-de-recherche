import random
import numpy as np
import util as ut

# Application de l'heuristique de Jackson pour avoir une solution de départ réalisable
# Prend à chaque début d'intervalles les taches qui ont les di les plus petits
def jackson_heuristique(tasks):
    nodes_list = []
    sorted_ddl = np.argsort(tasks["di"])
    for t in range(n):
        for k in range(len(intervals_list)):
            it = intervals_list[k]
            long_int = it[1]-it[0]
            if (tasks["ri"][t]<=it[0] and tasks["di"][t]>=it[1]):
                nodes_list.append(((str(t+1), "I"+str(k+1), dict(weight=0,capacity=long_int))))
    pass


# Initialisations
n,m = 10, 3
alpha, beta =0,0
while (alpha==0 or beta==0):
    alpha, beta = random.random(), random.random()
ri, qi, pi = ut.generer_exemple(n,m, alpha, beta)
a = [x+y+z for (x,y,z) in zip(ri, qi, pi)]
C = max(a)
di = [C - x for x in qi]
print("di :", di)

tasks = {"ri":ri,
        "di" :di,
        "pi" :pi}
intervals__values = list(dict.fromkeys(tasks["ri"] + tasks["di"]))
intervals_list = ut.createIntervals(intervals__values)

print(np.argsort(tasks["di"]))
print(np.sort(tasks["di"]))
