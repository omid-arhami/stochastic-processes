# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 10:33:20 2020

@author: Omid Arhami

Codes for Chapter 7.2 A Single-Server Queueing System

Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X

"""
from numpy import random, Infinity, array, mean
from math import log
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# 1- Time Variable:
# t

# 2- Counter Variables:
# NA: the number of arrivals (by time t)
# ND: the number of departures (by time t)

# 3- System State Variable:
# n: the number of customers in the system (at time t)

# 4- Event list:
# tA :the time of the next arrival (after t)
# tD : the service completion time of the customer presently being served

# 5- The output variables:
# A[i], the arrival time of customer i
# D[i], the departure time of customer i
# Tp, the time past T
# Q_len(n, t) : the number of customers in the system at each point of time


# customers arrive in accordance with a nonhomogeneous Poisson process
def tA_gen(t, lam, T):
    lam_0 = -minimize_scalar(lambda x : -lam(x), lam(T), bounds=(0, T), method='bounded')['fun']
    t0 = -log(random.uniform())/lam_0
    u = random.uniform()
    while u > lam(t + t0)/lam_0 :
        t0 = -log( random.uniform() )/lam_0
        u = random.uniform()
    x = t + t0
    return(x)


# Distribution of service time
def tService_Gen(mu, service_time_std):
    return( max(0, mu + service_time_std * random.uniform()) )
 

# Initialize:
numsim = 10**2
T = 10
lam = lambda x : T**2 / 4 - (x - T/2)**2 /2 + 0.05 * T
t = 0
n = 0
A = []
D = []
NA = len(A)
ND = len(D)
tA = tA_gen(t, lam, T)
tD = Infinity
Q_len = [[t, n]]
# Customer service time:
mu = 0.03
service_time_std = 0.01


while n >= 0:
    
    if (min(tA,tD) <= T) & (tA <= tD) :
        t = tA
        n += 1
        A.append(tA)
        Q_len.append([t, n])
        if n == 1 :
            tD = t + tService_Gen(mu, service_time_std)
        tA = tA_gen(t, lam, T)

    if (min(tA,tD) <= T) & (tA > tD) :
        t = tD
        n -= 1
        D.append(tD)
        Q_len.append([t, n])
        if n > 0 :
            tD = t + tService_Gen(mu, service_time_std)
        else:
            tD = Infinity
       
    if (min(tA,tD) > T) & (n > 0) :
        t = tD
        n -= 1
        D.append(tD)
        Q_len.append([t, n])
        if n > 0 :
            tD = t + tService_Gen(mu, service_time_std)

    if (min(tA,tD) > T) & (n == 0) :
        Tp = t
        n -= 1


NA = len(A)
ND = len(D)
t_extra_work = max([0, t - T])
print(
    "t = ", t, "\n", "\n",
    "t_extra_work = ", t_extra_work
)

A = array(A)
D = array(D)
Delays = D-A
print("Average waiting time for each customer=", mean(Delays) )

Q_len = pd.DataFrame(Q_len)
plt.plot(Q_len[0], Q_len[1], label="Queue length")
plt.legend(loc="best")
plt.show()