# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:14:30 2020

@author: Omid Arhami

Example 9c: Simulating a Queueing System
Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X

A Single-Server Queueing System with Antithetic Variables

"""
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

numsim = 10**3

# 1- Time Variable:
# t

# 2- Counter Variables:

# 3- System State Variable:
# n: the number of customers in the system (at time t)

# 4- Event list:
# tA :the time of the next arrival (after t)
# tD : the service completion time of the customer presently being served

# 5- The output variables:
# A[i], the arrival time of customer i
# D[i], the departure time of customer i
# Tp, the time past T

# customers arrive in accordance with a homogeneous Poisson process
def tA_gen( lam, u):
    return(- math.log(u)/lam)
    
# Distribution of service time
def tService_Gen(mean, service_time_std, u):
    return( np.maximum(0, mean + service_time_std*u) )
 
# Initialize:
T = 1000
lam = 1

t = 0
n = 0
A = []
D = []
tA = tA_gen( lam, np.random.uniform() )
tD = np.Infinity
# Customer service time:
mean = 0.3
service_time_std = 0.15


while n >= 0:
    
    if (np.minimum(tA,tD) <= T) & (tA <= tD) :
        t = tA
        n += 1
        A.append(tA)
        if n == 1 :
            u10 = np.random.uniform()
            tD = t + tService_Gen(mean, service_time_std, u10)
        u11 = np.random.uniform()
        tA = t + tA_gen( lam, u11)


    if (np.minimum(tA,tD) <= T) & (tA > tD) :
        t = tD
        n -= 1
        D.append(tD)
        if n > 0 :
            u12 = np.random.uniform()
            tD = t + tService_Gen(mean, service_time_std, u12)
        else:
            tD = np.Infinity
        
       
    if (np.minimum(tA,tD) > T) & (n > 0) :
        t = tD
        n -= 1
        D.append(tD)
        if n > 0 :
            u13 = np.random.uniform()
            tD = t + tService_Gen(mean, service_time_std, u13)
            
    
    if (np.minimum(tA,tD) > T) & (n == 0) :
        Tp = t
        n -= 1


A = np.array(A)
D = np.array(D)
Delays = D-A
#print("Average waiting time=", np.mean(Delays) )
print("Standard deviation of waiting time=", np.std(Delays) )


###############
#################### Do it again with Antithetic Variables: ########## 
###############

# Initialize:

t = 0
n = 0
A = []
D = []
tA = tA_gen( lam, np.random.uniform() )
tD = np.Infinity
# Customer service time:
mean = 0.3
service_time_std = 0.15

c10 = 0 # to swap u and 1-u
c11 = 0 # to swap u and 1-u
c12 = 0 # to swap u and 1-u
c13 = 0 # to swap u and 1-u

while n >= 0:
    
    if (np.minimum(tA,tD) <= T) & (tA <= tD) :
        t = tA
        n += 1
        A.append(tA)
        if n == 1 :
            if c10%2 == 0 :
                u10 = np.random.uniform()
                tD = t + tService_Gen(mean, service_time_std, u10)
                c10 += 1
            else:
                tD = t + tService_Gen(mean, service_time_std, 1-u10)
                c10 += 1
        if c11%2 == 0 :
            u11 = np.random.uniform()
            tA = t + tA_gen( lam, u11)
            c11 += 1
        else:
            tA = t+ tA_gen( lam, 1-u11)
            c11 += 1

    if (np.minimum(tA,tD) <= T) & (tA > tD) :
        t = tD
        n -= 1
        D.append(tD)
        if n > 0 :
            if c12%2 == 0 :
                u12 = np.random.uniform()
                tD = t + tService_Gen(mean, service_time_std, u12)
                c12 += 1
            else:
                tD = t + tService_Gen(mean, service_time_std, 1-u12)
                c12 += 1
        else:
            tD = np.Infinity

    if (np.minimum(tA,tD) > T) & (n > 0) :
        t = tD
        n -= 1
        D.append(tD)
        if n > 0 :
            if c13%2 == 0 :
                u13 = np.random.uniform()
                tD = t + tService_Gen(mean, service_time_std, u13)
                c13 += 1
            else:
                tD = t + tService_Gen(mean, service_time_std, 1-u13)
                c13 += 1
            
    if (np.minimum(tA,tD) > T) & (n == 0) :
        Tp = t
        n -= 1

A = np.array(A)
D = np.array(D)
Delays = D-A
#print("Average waiting time with Antithetic Variables=", np.mean(Delays) )
print("Standard deviation of waiting time with Antithetic Variables=", np.std(Delays) )