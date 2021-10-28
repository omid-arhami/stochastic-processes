# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:45:20 2020

@author: Omid Arhami

Question 6, Chapter 7 of the Simulation book by Sheldon Ross, 2013
DOI: https://doi.org/10.1016/C2011-0-04574-X

7.6 An Insurance Risk Model
"""
import numpy as np


# claims come according to independent Poisson processes with a common rate λ
# each claim amount has distribution F.
# new customers sign up according to a Poisson process with rate nu
# each existing policyholder remains with the company for an exponentially distributed time with rate mu
# each policy holder pays the insurance firm at a fixed rate c per unit time.
# 
# 
# 
# Variables:
# Time variable:
#   t

# System state:
#   n : the total number of customers at t
#   a : total capital

# Counter variables:

# Events:
#   new claim, each with rate lambda
#   new customer joins, rate nu
#   customer churns, each with rate mu

# Eventlist:
#	tE : the time at which the next event occurs

# Output:
# I : 1, if the firm’s capital is nonnegative throughout [0, t]

def claimGen(claim_avg, claim_var) :
    Y = np.maximum(0, claim_avg + claim_var * np.random.randn())
    return(Y)


def tE_gen(t, param) :
    u = np.random.uniform()
    t = t - np.log(u)/param
    return(t)


def eventDeterminator(lam, mu, nu, n) :
    u = np.random.uniform()
    if u <= n*mu / (nu + n*lam + n*mu) :
        J = 2
    elif (u > n*mu / (nu + n*lam + n*mu)) & (u <= n*lam / (nu + n*lam + n*mu)) :
        J = 3
    else:
        J = 1
    return(J)

# Global initializations:
T = 1000
n0 = 10
a0 = 1
c = 0.05
claim_avg = 100000
claim_var = 15000
lam = 2 # claims
nu = 5  # new customers
mu = 3 # lost customers
numsim = 10


def insuranceSim(T, n0, a0, c):
    # Initialize:
    t = 0
    n = n0
    a = a0
    I = 1
    tE =  tE_gen(t, nu + n*lam + n*mu)
    
    while tE <= T:
        a += (tE - t) * c * n
        t = tE
        J = eventDeterminator(lam, mu, nu, n)
        if J == 1 :
            n += 1
        elif J == 2 :
            n -= 1
        elif J == 3 :
            claim_value = claimGen(claim_avg, claim_var)
            a -= claim_value
            if a <= 0:
                I = 0
                break
        tE = tE_gen(t, nu + n*lam + n*mu)
    
    return(I)
            
res = np.array( [insuranceSim(T, n0, a0, c) for x in range(numsim)] )
p = np.sum(res)/numsim
print("The probability of no bankrupcy = ", p) 
    