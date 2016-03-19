# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:50:08 2016

@author: yanshen0
"""

import matplotlib
import numpy as np
import pylab as plt


def int_ran(N):               #return a random integer from 0 to N
    rand = np.random.uniform(0.0, N)
    for i in range(N):
        if rand > i and rand <= i+1:
            rand = i
    return rand        




nx = 60   #I am using 60*40, 600*400 would take too long...
ny = 40

gas_distribution = np.zeros((nx,ny))

for i in range(int(nx/3)):
    gas_distribution[i,:] = 1  #gas A
for i in range(int(2*nx/3),nx):
    gas_distribution[i,:] = -1  #gas B


import matplotlib.cm as cm

plt.figure()             #plot original distribution
fig = plt.imshow(gas_distribution, cmap=cm.RdYlGn)
plt.show()




step_total = 1e6    #random walk step
time = 0

#random walk
while time < step_total:
    xr = int_ran(nx)
    yr = int_ran(ny)
    x_old = xr
    y_old = yr
    
    if gas_distribution[xr,yr] == 0:
        continue
    
    r = np.random.uniform(0.0,1.0)
    if r <= 0.25:
        yr = yr + 1
    elif r>0.25 and r<=0.5:
        yr = yr - 1
    elif r>0.5 and r<=0.75:
        xr = xr - 1
    else:
        xr = xr + 1
    
    if xr < 0 or xr >= nx or yr < 0 or yr >= ny:  #stay in the box
        continue
    
    if gas_distribution[xr,yr] !=0:    # reject if already occupied
        continue
    else:
        gas_distribution[xr,yr] = gas_distribution[x_old,y_old]
        gas_distribution[x_old,y_old] = 0
    
    time = time + 1
    

plt.figure()
fig = plt.imshow(gas_distribution, cmap=cm.RdYlGn)
plt.show()
  
    
    
    
    
    