# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 23:38:11 2020

@author: omid Arhami

Question 17, Chapter 7 of the Simulation book by Sheldon Ross, 2013
DOI: https://doi.org/10.1016/C2011-0-04574-X

Estimate, by a simulation study, the expected worth of owning an option
to purchase a stock anytime in the next 20 days for a price of 100 if the
present price of the stock is 100.
"""
from numpy import random, exp, mean, sqrt, pi, log
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

# Sn :  denotes the price of a specified stock at the end of day n.
# Sn = S0 * exp{X1 +· · ·+ Xn}
# Xi : is a sequence of independent normal random variables, each with mean mu and variance s^2
# K : option to purchase one unit of this stock at a fixed price K.
# N : at the end of any of the next N days.
# E[SP] − K = ???

# Two equal series:
# S_0 , S_1 ,  ... , S_N
# P_N , P_N-1, ... , P_0

numsim = 10**3
N = 20
S0 = 100
K = 100
mu = -0.05
s = 0.3
#
alpha = mu + 0.5*s**2
if alpha < 0 :
    print("You need to use this policy from the text.")
else:
    print("You do NOT need to use this policy from the text.")

def phi(x):
    a1 = 0.4361836
    a2 = -0.1201676
    a3 = 0.9372980
    if x >= 0 :
        y = 1/(1 + 0.33267 * x)
        phi = 1 - (1/sqrt(2*pi)) * (a1*y + a2*y**2 + a3*y**3)*exp(-x**2 / 2)
    else:
        y = 1/(1 - 0.33267 * x)
        phi = 1 - (1 - (1/sqrt(2*pi)) * (a1*y + a2*y**2 + a3*y**3)*exp(-x**2 / 2))
    return(phi)

def optionExercising(K, S0, N, mu, s):
    S = pd.Series( [S0]*(N) )
    P = pd.Series( [S0]*(N) )
    Gain = 0
    # j counts the real days going forward
    # i is the i in the policy formula
    for j in range(1,N) : # In the policy m >= 1 so j < N
        S[j] = S[j-1] * exp( random.normal()*s + mu )
        m = N - j # In the policy m >= 1
        P[m] = S[j]
        is_greater = 1
        for i in range(1, m+1) :
            b = (i * mu - log(K/P[m]))/(s * sqrt(i))
            if (P[m] <= K + P[m] * exp(i*alpha) * phi(s * sqrt(i) + b) - K * phi(b)) :
                is_greater = 0
        if (P[m] > K) & (is_greater == 1):
            Gain = P[m] - K
            break
    return(Gain, S, j)

res = [optionExercising(K, S0, N, mu, s)[0] for t in range(numsim)]    
print("\n", "The expected worth of option =", mean(res) , "\n")


# A sample:
print("** A sample:")
sample = optionExercising(K, S0, N, mu, s)
gain = sample[0]
S = sample[1]
# Exercising day:
j = sample[2]
if gain :
    print("Exercising day:",j)
print("The expected worth =", gain, "\n")
plt.plot(S)
plt.show()
