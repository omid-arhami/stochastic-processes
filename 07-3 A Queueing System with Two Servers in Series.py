# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 19:56:20 2020

@author: Omid Arhami

Codes for Chapter 7.3 A Queueing System with Two Servers in Series

Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X

"""
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt


# 1- Time Variable:
# t

# 2- Counter Variables:
# NA: the number of arrivals (by time t)
# ND: the number of departures (by time t)

# 3- System State Variable:
# n1: the number of customers at server 1 (at time t)
# n2: the number of customers at server 2 (at time t)

# 4- Event list:
# tA : The time of the next arrival (after t)
# t1 : The service completion time (not duration) of the customer presently being served by server 1
# t2 : The service completion time (not duration) of the customer presently being served by server 2


# 5- The output variables:
# A1[i], the arrival time of customer i at server 1
# A2[i], the arrival time of customer i at server 2
# D[i], the departure time of customer i


# customers arrive in accordance with a homogeneous Poisson process
def tA_gen(t, lam):
    t = t - math.log( np.random.uniform() )/lam
    return(t)


# Distribution of service time for server 1 or 2:
def tService_Gen(mean, service_time_std):
    return( np.maximum(0, mean + service_time_std*np.random.uniform()) )
 
    
# Initialize:

lam = 3
t = 0
n1 = 0
n2 = 0
A1 = []
A2 = []
D = []
NA = 0
ND = 0
tA = tA_gen(t, lam)
t1 = np.Infinity
t2 = np.Infinity
queue_1 = [[t, n1]]
queue_2 = [[t, n2]]
# Customer service time:
mean_1 = 0.1
service_time_std_1 = 0.03
mean_2 = 0.25
service_time_std_2 = 0.15
    
# Soppose we're going to service 100 customers:
total_custmers = 100

while ND <= total_custmers :
    
    if tA == np.min([tA, t1, t2]) :
        if (NA < total_custmers) :
            t = tA
            n1 += 1
            NA += 1
            A1.append(t)
            queue_1.append([t,n1])
            queue_2.append([t,n2])
            if n1 == 1:
                t1 = t + tService_Gen(mean_1, service_time_std_1)
            tA = tA_gen(t, lam)
        else:
            tA = np.Infinity
        
        
    if (t1 <= t2) & (t1 < tA) :
        t = t1
        n1 -= 1
        n2 += 1
        A2.append(t)
        queue_1.append([t,n1])
        queue_2.append([t,n2])
        if n1 == 0:
            t1 = np.Infinity
        else:
            t1 = t + tService_Gen(mean_1, service_time_std_1)
        
        if n2 == 1 :
            t2 = t + tService_Gen(mean_2, service_time_std_2)
        
        
    if (t2 < t1) & (t2 < tA) :
        t = t2
        ND += 1
        n2 -= 1
        D.append(t)
        queue_1.append([t,n1])
        queue_2.append([t,n2])
        if n2 == 0 :
            t2 = np.Infinity
        else:
            t2 = t + tService_Gen(mean_2, service_time_std_2)
        if ND == total_custmers :
            break
        
A1 = np.array(A1)
D = np.array(D)
Delays = D-A1
print("Average waiting time for each customer=", np.mean(Delays) )
1
queue_1 = pd.DataFrame(queue_1)
queue_2 = pd.DataFrame(queue_2)

plt.plot(queue_1[0], queue_1[1], label="queue 1")
plt.plot(queue_2[0], queue_2[1], 'r:', label="queue 2")
plt.legend()
plt.show()

       