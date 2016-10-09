import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import math
import random

from pprint import pprint

BOUND_MAX = 2**4
L_LENGTH = 10000
SL_LENGTH = 5
NB_INSERT = 6
NB_STD = 4

print "generation..."

L   = [random.randrange(0, BOUND_MAX) for i in range(L_LENGTH)]  #the long sequence
SL  = [random.randrange(0, BOUND_MAX) for i in range(SL_LENGTH)] #the shorter sequence
idx = [random.randrange(0, L_LENGTH) for i in range(NB_INSERT)]  #index in the lonsequence to appen the shorter
idx.sort()


for i in idx:
    L = L[:i] + SL + L[i:]

print "searching..."


d = {}
for i in range(len(L) - 2): #-1):#- 2):
    tpl = ((L[i], L[i + 1]), L[i + 2]) #(L[i], L[i + 1]) #((L[i], L[i + 1]), L[i + 2])
    if tpl in d:
        d[tpl] += 1
    else:
        d[tpl] = 1


a = np.array(d.values())
a.sort()

#keep number bigger than 6 standard deviation (cf. anomally detection)
#keep keys in d that have a counter bigger than NB_STD * std
dd = {}
for k in d:
    if d[k] >= a.mean() + NB_STD * a.std():
        dd[k] = d[k]

#remap and keep the keys
dd = {(a, b, c) : [] for ((a, b), c) in dd.keys()}

#create all possibles paths
for (a, b, c) in dd:
    dd[(a, b, c)] = filter(lambda t: (b, c) == (t[0], t[1]), dd.keys())

#get the longest path without cycle --> should be the SL (or close to, statistically)
longest = []

visited = set()
path = []
def search(v, d={}):
    visited.add(v)
    path.append(v)
    
    if len(path) > len(longest):
        longest[:] = path[:]
        
    for w in d[v]:
        if w not in visited:
            search(w, d)
            
    path.pop()
    visited.remove(v)

#try all possibilities
for v in dd:
    search(v, dd)

#remake the list of longest
L = list(longest[0])
for t in longest[1:]:
    L.append(t[2])

print L == SL
print L
print SL


