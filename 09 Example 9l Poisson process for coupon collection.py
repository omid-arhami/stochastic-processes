# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 13:07:51 2020

@author: Omid Arhami

Example 9l a Poisson process for coupon collection:
Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X

- Suppose there are r types of coupons and that every new coupon
collected is, independently of those previously collected, type i with 
probability pi ,

- the times at which coupons are collected constitute the event times of 
a Poisson process with rate λ = 1.

- N denoting the number of coupons "needed" so that we have collected
ni or more type i coupons,

E[N] = ?

"""
from numpy import random, array, arange, log, prod, mean, exp
from math import factorial

nsim = 10**2
r = 10
p_i = array([1/r for x in range(r)])
n_i = 3*arange(r) + 10
lam = 1
m = int(mean(n_i) * r)

#

# a)
# After conditioning on T = (T1, . . . , Tr ):
# E[N|T]  = T + n − sum(p_i*T_i)
def coupons_N(r, p_i, n_i, lam):
    n = sum(n_i)
    T_i = [-log(prod(random.rand(r)))/lam for x in range(r)]
    T = max(T_i)
    EN = n + T - sum(p_i * T_i)
    return(EN)

EN = mean([coupons_N(r, p_i, n_i, lam) for x in range(nsim)])
print("E[N] =", EN)

# b)
# P[N>m | T] = P[X > m-n]
# = 1 - sum( exp(-lam_T) * lam_T**i / factorial(i) )
# X ~ Poiss(lam_T)
# lam_T = sum(p_i * (T - T_i))
def coupons_N_m(r, p_i, n_i, lam, m):
    n = int( sum(n_i) )
    T_i = [-log(prod(random.rand(r)))/lam for x in range(r)]
    T = max(T_i)
    lam_T = sum(p_i * (T - T_i))
    sp = [exp(-lam_T) * lam_T**i / factorial(i) for i in range(m-n+1)]
    P_N_m = 1 - sum(sp)
    return(P_N_m)

P_N_m = mean([coupons_N_m(r, p_i, n_i, lam, m) for x in range(nsim)])
print("P[N > m] =", P_N_m)