# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:28:03 2020

@author: omid Arhami

Question 5, Chapter 9 of the Simulation book by Sheldon Ross, 2013
DOI: https://doi.org/10.1016/C2011-0-04574-X

Antithetic variables:

θ = E[Z**3 * e**Z]
θ is monotone
Z is a standard normal random variable
2μ − Z = -Z is also normal and negatively correlated with Z

"""
from numpy import exp, random, mean, var
numsim = 10**5

def theta(Z):
    t = Z**3 * exp(Z)
    return(t)


Z = random.normal(loc=0.0, scale=1.0, size=numsim)
X = theta(Z)
print("Regular way:")
print("θ =", mean(X))
print("Var=", var(X))
Y = theta(-Z)

res1 = (X+Y)/2
print("\n", "with Antithetic Variables & pairing:")
print("θ =", mean(res1))
print("Var=", var(res1))

Z2 = random.normal(loc=0.0, scale=1.0, size=numsim//2)
res3 = []
res3.append(theta(Z2))
res3.append(theta(-Z2))
print("\n","with Antithetic Variables:")
print("θ =", mean(res3))
print("Var=", var(res3))
