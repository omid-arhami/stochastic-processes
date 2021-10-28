# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 21:41:22 2020

@author: Omid Arhami

Codes for Chapter 5.5 Generating a Nonhomogeneous Poisson Process
Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X


Thinning method:
lambda: [0,T] ---> [0,inf)
lam_0 >= lambda(t)   for all t

"""
import numpy as np
import math
import pandas as pd
import time
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

numsim = 10**2
T = 10
t1 = time.time()

def nonHomPois(lam, T):
    lam_0 = -minimize_scalar(lambda x : -lam(x), lam(T), bounds=(0, T), method='bounded')['fun']
    t = 0
    N = 0
    s = []
    while t <= T:
        u1 = np.random.uniform()
        t = t - math.log(u1)/lam_0
        if t<= T:
            u2 = np.random.uniform()
            if u2 <= lam(t)/lam_0 :
                N += 1
                s.append(t)
    return(N, np.array(s))        


lam = lambda t : t + 10

res1 = []
for i in range(numsim) :
    res1.append(nonHomPois(lam, T)[1])

t2 = time.time()
print("Run time 1: ", t2-t1)

res1 = pd.DataFrame(res1)
res1 = np.array(res1).reshape(res1.shape[0]*res1.shape[1])
res1 = pd.Series(res1).dropna()

plt.hist(res1, bins=10, rwidth=0.88)
plt.show()
# chart should go from 10*numsim to 20*numsim linearly.
