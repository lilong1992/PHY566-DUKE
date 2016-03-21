# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:08:58 2016

@author: lilon
can mix the gas in one minute
2-stage mixing
1st stage:large step
2nd stage:one step
"""
import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm


def move_random(steps): #pick one particle and move steps steps
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,160000-1)
    i = available[pick][0]
    j = available[pick][1]
    dice=rd.random()
    if dice<0.25:
        if j-steps>=0 and u[i,j-steps]==0: #left
            u[i,j-steps]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j-steps] #renew the position
    elif dice<0.5:
        if j+steps<W and u[i,j+steps]==0: #right
            u[i,j+steps]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j+steps]
    elif dice<0.75:
        if i-steps>=0 and u[i-steps,j]==0: #down
            u[i-steps,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i-steps,j]
    else:
        if i+steps<H and u[i+steps,j]==0: #up
            u[i+steps,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i+steps,j]
        

# initialize u
H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
u = np.zeros((H,W))
available = np.zeros((160000,2)) #store positions of all particles
for i in range(H):
    for j in range(W/3):
        u[i,j] = -1
        available[i*W/3+j]=[i,j]
    for j in range(2*W/3,W):
        u[i,j] = 1
        available[i*W/3+j+79600]=[i,j]


# mixing gases
for m in range(10001):
    for n in range(1000):
        steps=rd.randint(50,150)
        move_random(steps)
    if m%500==0:
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)  # which color map looks better??
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
        plt.yticks((0,200,400),('0','200','400'),fontsize=14)
        plt.title('Mixing two gases',fontsize=22,fontweight='bold')
        plt.savefig('Xgas_mixing_step#'+str(m)+'e3.png')
        plt.close()

