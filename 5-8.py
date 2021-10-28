# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 22:12:44 2020

@author: omid Arhami

Question 8, Chapter 5 of the Simulation book by Sheldon Ross 
DOI: http://dx.doi.org/10.1016/B978-0-12-415825-2.00005-X

give algorithms for generating random variables from the following distributions.
"""
from numpy import random, log, cumsum, vectorize
import matplotlib.pyplot as plt

nsim = 10**4
# (a)
def f8a():
    u1 = random.uniform()
    if u1 <= 1/3 :
        X = random.uniform()
    elif 1/3 < u1 <= 2/3 :
        X = random.uniform()**(1/3)
    elif u1 > 2/3 :
        X = random.uniform()**(1/5)
    return(X)
    
res_a = [f8a() for n in range(nsim)]
# f(x) = (1/3)*(1 + 3*x**2 + 5*x**4)
# similar to hist
plt.figure(1)
plt.hist(res_a, rwidth=0.88)


# (b)
# These F1 & F2 have the needed differential (density function)
# F1(x) = (1 - exp(-2*x))    x > 0
# F2(x) = x                  0<x<1
# F(x) = (1/3)*F1(x) + (2/3)*F2(x)

def F1():
    u = random.uniform()
    x = -log(u) / 2
    return(x)

def F2():
    x = random.uniform()
    return(x)

def f8b(U):
    if U <= (1/3) :
        x = F1()
    else:
        x = F2()
    return(x)

f8b_v = vectorize(f8b)    
U = random.rand(nsim)
X = f8b_v(U)
plt.figure(2)
plt.hist(X, rwidth=0.88, bins=65)
plt.show()


# (c) :
n=  20
alpha = [1/n]*n

def f8c(alpha):
    n = len(alpha)
    alfa_cum = cumsum(alpha)
    u = random.uniform()
    for tr in range(n):
        if alfa_cum[tr] >= u :
            i = tr+1
            break
    x = (random.uniform())**(1/i)
    return(x)
    
res_c = [f8c(alpha) for n in range(nsim)]
plt.figure(3)
plt.hist(res_c, rwidth=0.88, bins=45)