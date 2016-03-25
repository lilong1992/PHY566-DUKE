# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:08:58 2016

@author: lilon
get rid of the boundary condition by adding an unmovable boundary
now it's 402*602
"""
import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm


def move_random(): #pick one particle and move 1 step
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,160000-1)
    i = available[pick][0]
    j = available[pick][1]
    dice=rd.random()
    if dice<0.25:
        if u[i,j-1]==0: #left
            u[i,j-1]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j-1] #renew the position
    elif dice<0.5:
        if u[i,j+1]==0: #right
            u[i,j+1]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j+1]
    elif dice<0.75:
        if u[i-1,j]==0: #down
            u[i-1,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i-1,j]
    else:
        if u[i+1,j]==0: #up
            u[i+1,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i+1,j]
        

# initialize u
H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
u = np.ones((H+2,W+2))
available = np.zeros((160000,2)) #store positions of all particles
for i in range(1,H+1):
    for j in range(1,W/3+1):
        u[i,j] = -1
        available[(i-1)*W/3+j-1]=[i,j]
    for j in range(201,401):
        u[i,j]=0
    for j in range(2*W/3+1,W+1):
        u[i,j] = 1
        available[(i-1)*W/3+j-1+79600]=[i,j]


# mixing gases
for m in range(500001):
    for n in range(10000):
        move_random()
    if m%5000==0:
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)  # which color map looks better??
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,602),('0','200','400','602'),fontsize=14)
        plt.yticks((0,201,402),('0','201','402'),fontsize=14)
        plt.title('Mixing two gases',fontsize=22,fontweight='bold')
        plt.savefig('Ygas_mixing_step#'+str(m)+'e4.png')
        plt.close()

