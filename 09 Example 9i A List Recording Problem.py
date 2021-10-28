# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:07:43 2020

@author: Omid Arhami

Example 9i A List Recording Problem
Simulation, Fifth Edition by Sheldon M. Ross(2013)
DOI: https://doi.org/10.1016/C2011-0-04574-X
"""
from numpy import floor, random, cumsum, var, mean, arange, array

numsim = 10**2
################# The “natural” way: ########
N = 50 # number of requests
n = 10 # length of numbers list
n_sum = sum(arange(n))
p = [x/n_sum for x in range(n)] # the request is for element i with probability p(i)

def permutationGen(n):
    p = [x for x in range(n)]
    k = n-1
    while k > 0 :
        u = random.uniform()
        i = floor((k+1) * u).astype(int) # i between 0 to k
        temp = p[k]
        p[k] = p[i]
        p[i] = temp
        k -= 1
    return(p)

def requestGenerator(p): # p is the probability array
    n = len(p)
    F = cumsum(p)
    u = random.uniform()
    for i in range(n):
        if F[i] > u :
            req = i
            break
    return(req)

def simulator1(n, p, N):
    sum_1 = 0
    n_array = permutationGen(n)
    for t in range(N):
        request_for_value = requestGenerator(p)
        index = n_array.index(request_for_value)
        sum_1 += index
        if index > 0 :
            temp = n_array[index]
            n_array[index] = n_array[index-1]
            n_array[index-1] = temp
    return(sum_1)

results = [simulator1(n , p, N) for i in range(numsim)]    
print("Avg of the Sum of positions=", mean(results))
print("Variance=", var(results))

####################### Using control variables: #########
# use SUM(U_r) as a control variable, where U_r is the random number
# used for the rth request in a run    
# SUM(position) is main variable.
def requestGenerator_VR(p, u):
    n = len(p)
    F = cumsum(p)
    for i in range(n):
        if F[i] > u :
            req = i
            break
    return(req)

def simulator_control_variate(n , p, N):
    sum_2 = 0
    sum_U = 0
    n_array = permutationGen(n)
    for t in range(N):
        u = random.uniform()
        sum_U += u
        p_present_ordering = [p[n_array[k]] for k in range(n)]# p(i_k) = p[n_array(k)]
        request_for_value = requestGenerator_VR(p_present_ordering, u)
        index = n_array.index(request_for_value)
        sum_2 += index
        if index > 0 :
            temp = n_array[index]
            n_array[index] = n_array[index-1]
            n_array[index-1] = temp
    return(sum_2, sum_U) # X & Y

X = [simulator_control_variate(n , p, N)[0] for t in range(numsim)]
Y = [simulator_control_variate(n , p, N)[1] for t in range(numsim)]
X = array(X)
Y = array(Y)
c_star = -(mean(X*Y) - mean(X)*mean(Y) )/( mean(Y**2)- mean(Y)**2 )

res2 = [X[t] + c_star*(Y[t] - N/2 ) for t in range(numsim)]
print("Variance of control variate method:" , var(res2))
print("The theoritical difference is:", -(mean(X*Y) - mean(X)*mean(Y) )**2 /( mean(Y**2)- mean(Y)**2 ) )
