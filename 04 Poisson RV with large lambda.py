# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 10:20:46 2020

@author: Omid Arhami

Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X
Chapter 04, Creating a Poisson RV with large lambda
"""
import numpy as np
import math
import time

lam = 50
numsim = 10*7

def pois(lam):
    p = math.exp(-lam)
    i = 0
    F = p
    u = np.random.uniform()
    while F <= u:
        p = p * lam / (i+1)
        F += p
        i += 1
    return(i)
    
# Normal way:
t1 = time.time()
res1 = [pois(lam) for t in range(numsim)]
t2 = time.time()
print("Runtime of Normal way:", t2 - t1 )
print("mean=", np.mean(res1))

# Better way:
def pois_upward(lam, I, u, p_I, S_I):
    p = p_I
    i = I
    F = S_I
    while F <= u:
        p = p * lam / (i+1)
        F += p
        i += 1
    return(i)

def pois_downward(lam, I, u, p_I, S_I):
    p = p_I
    i = I
    F = S_I
    while F > u:
        F -= p
        i -= 1
        p = p * (i+1)/lam
    return(i + 1)

t3 = time.time()
I = int( np.floor(lam) )
p = [math.exp(-lam)]
for i in range(I) :
    p.append(p[i]*lam/(i + 1))
F = np.cumsum(p)
p_I = p[-1]
S_I = F[-1]

res2 = np.zeros(numsim)
for t in range(numsim) :
    u = np.random.uniform()
    if u >= S_I :
        res2[t] = pois_upward(lam, I, u, p_I, S_I)
    elif u < S_I :
        res2[t] = pois_downward(lam, I, u, p_I, S_I)

t4 = time.time()
print("Runtime of Better way:", t4 - t3 )
print("mean 2=", np.mean(res2))