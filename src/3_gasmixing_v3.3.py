# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:08:58 2016

@author: lilon
by choosing large steps the gas mixes much faster
"""
import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm


def checkandget_random_direction(i,j):
    global u
    direc=[]
    if j-49>=0 and u[i,j-49]==0: #left
        direc.append(0)
    if j+49<W and u[i,j+49]==0: #right
        direc.append(1)
    if i-49>=0 and u[i-49,j]==0: #down
        direc.append(2)
    if i+49<H and u[i+49,j]==0: #up
        direc.append(3)
    if len(direc)==0:
        return -1
    else:
        return direc[rd.randint(0,len(direc)-1)]


def move(): #pick one particle and move one step
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,160000-1)
    i = available[pick][0]
    j = available[pick][1]
    dice=checkandget_random_direction(i,j)
    if dice==-1:
        return "unable to move"
    else:
        if dice==0:
            u[i,j-49]=u[i,j]
            available[pick]=[i,j-49] #renew the position
        elif dice==1:
            u[i,j+49]=u[i,j]
            available[pick]=[i,j+49]
        elif dice==2:
            u[i-49,j]=u[i,j]
            available[pick]=[i-49,j]
        else:
            u[i+49,j]=u[i,j]
            available[pick]=[i+49,j]
        u[i,j]=0



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
        plt.savefig('Vgas_mixing_step49#'+str(m)+'e2.png')


