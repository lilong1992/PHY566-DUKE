# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:08:58 2016

@author: lilon
not done yet
2-stage mixing
1st stage:large step
2nd stage:one step
time=50*1st_stage+2nd_stage 
"""
import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm


def move(): #pick one particle and move 10 steps
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,160000-1)
    i = available[pick][0]
    j = available[pick][1]
    dice=rd.random()
    if dice<0.25:
        if j-10>=0 and u[i,j-10]==0: #left
            u[i,j-10]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j-10] #renew the position
    elif dice<0.5:
        if j+10<W and u[i,j+10]==0: #right
            u[i,j+10]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j+10]
    elif dice<0.75:
        if i-10>=0 and u[i-10,j]==0: #down
            u[i-10,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i-10,j]
    else:
        if i+10<H and u[i+10,j]==0: #up
            u[i+10,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i+10,j]
        
def move1(): #pick one particle and move 1 step
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,160000-1)
    i = available[pick][0]
    j = available[pick][1]
    dice=rd.random()
    if dice<0.25:
        if j-1>=0 and u[i,j-1]==0: #left
            u[i,j-1]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j-1] #renew the position
    elif dice<0.5:
        if j+1<W and u[i,j+1]==0: #right
            u[i,j+1]=u[i,j]
            u[i,j]=0
            available[pick]=[i,j+1]
    elif dice<0.75:
        if i-1>=0 and u[i-1,j]==0: #down
            u[i-1,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i-1,j]
    else:
        if i+1<H and u[i+1,j]==0: #up
            u[i+1,j]=u[i,j]
            u[i,j]=0
            available[pick]=[i+1,j]
        
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
for m in range(40001):
    for n in range(100):
        move()
    if m%4000==0:
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)  # which color map looks better??
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
        plt.yticks((0,200,400),('0','200','400'),fontsize=14)
        plt.title('Mixing two gases',fontsize=22,fontweight='bold')
        plt.savefig('Wgas_mixing_step10#'+str(m)+'e2.png')


