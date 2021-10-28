# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:53:24 2020

@author: Omid Arhami

Codes for Chapter 12.2 The Hastings_Metropolis Algorithm
Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X

One way of simulating a sequence of random variables whose distributions
converge π( j ), j = 1, . . . ,m, is to find a Markov chain that is easy to simulate
and whose limiting probabilities are the π( j ). The Hastings–Metropolis algorithm
provides an approach for accomplishing this task. It constructs a time-reversible
Markov chain with the desired limiting probabilities, in the following manner.
"""
import pandas as pd
import numpy as np

TRIALS = 10**5

m = 5 # No. of states (from 0 to m-1)
b = [4, 2, 3, 1, 1] # probability(state i) = b[i] / Sum(b[i])

# STEP 1:
Q = [ [1/m]*m ]*m
k = m//2 # random initial state

# STEP 2x:
n = 0 # time
X = []
X.append(k)

# STEP 3:
while n <= TRIALS:
    # First we have to draw a random variable Y with distribution of the row X[n] of Q 
    F = np.cumsum(Q[X[n]-1]) # Because lists start from 0 
    u_y = np.random.uniform()
    for j in range(m):
        if F[j] >= u_y:
            Y = j+1 # Because lists start from 0 
            break
    #
    U = np.random.uniform()
    
# STEP 4:
    # Because lists start from 0 
    if U < ( (b[Y-1] * Q[Y-1][X[n]-1]) / (b[X[n]-1] * Q[X[n]-1][Y-1] ) ) :
        NextState = Y
    else:
        NextState = X[n]
# STEP 5:
    n+=1
    X.append(NextState)

# reporting:
X = pd.Series(X)
print(X.value_counts().sort_index()/len(X))