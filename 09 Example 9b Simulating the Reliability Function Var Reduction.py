# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:17:27 2020

@author: Omid Arhami

Example 9b: 
Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X

Simulating the Reliability Function + Variance reduction: k-of-n system

"""
import numpy as np

numsim = 10**2
k = 10 # minimum needed working components
n = 20 # total components
p = 0.5 # working probability of each component
Phi = 1 # working probability of the system

def k_of_n(n, k, p, U):
    S = [ U <= p ]
    if np.sum(S) >= k :
        Phi = 1
    else:
        Phi = 0
    return(Phi)

res1 = []
for i in range(numsim):
    U = np.random.rand(n)
    res1.append(k_of_n(n, k, p, U))

res2 = []
for i in range(numsim//2):
    U = np.random.rand(n)
    res2.append(k_of_n(n, k, p, U))
    res2.append(k_of_n(n, k, p, 1-U))

print("Working probability of the system=", np.mean(res1))
print("STD of the system=", np.std(res1))
print()
print("with Antithetic Variables : ")
print("Working probability of the system=", np.mean(res2))
print("STD of the system=", np.std(res2))