# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:08:58 2016

@author: lilon

modified from v2 by Long Li
cheat a little, still very slow
hope you can find some ideas from my code
"""
import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm

def add_new_avaliablesite(i,j):#the hole is at i,j
    global available,u
    if j-1>=0: #left of the hole
        if u[i,j-1] <> 0 and available.count([i,j-1])==0: #make sure it's not in the available list
            available.append([i,j-1])
    if j+1<W:
        if u[i,j+1] and available.count([i,j+1])==0:
            available.append([i,j+1])
    if i+1<H:
        if u[i+1,j] and available.count([i+1,j])==0:
            available.append([i+1,j])
    if i-1>=0: #down of the hole
        if u[i-1,j] and available.count([i-1,j])==0:
            available.append([i-1,j])

def checkandget_random_direction(i,j):
    global u
    direc=[]
    if j-1>=0 and u[i,j-1]==0: #left
        direc.append(0)
    if j+1<W and u[i,j+1]==0: #right
        direc.append(1)
    if i-1>=0 and u[i-1,j]==0: #down
        direc.append(2)
    if i+1<H and u[i+1,j]==0: #up
        direc.append(3)
    if len(direc)==0:
        return -1
    else:
        return direc[rd.randint(0,len(direc)-1)]


def move(): #pick one particle and move one step
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,len(available)-1)
    i = available[pick][0]
    j = available[pick][1]
    dice=checkandget_random_direction(i,j)
    if dice==-1:
        return "unable to move"
    else:
        if dice==0:
            u[i,j-1]=u[i,j]
        elif dice==1:
            u[i,j+1]=u[i,j]
        elif dice==2:
            u[i-1,j]=u[i,j]
        else:
            u[i+1,j]=u[i,j]
        u[i,j]=0
        available.remove([i,j]) #i,j is no longer a particle
        add_new_avaliablesite(i,j) #add new particles that can move


# initialize u
H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
u = np.zeros((H,W))
for i in range(H):
    for j in range(W/3):
        u[i,j] = -1
    for j in range(2*W/3,W):
        u[i,j] = 1

# initialize available sites

available = []
for i in range(H):
    available.append([i,W/3-1])  # available sites at the beginning
    available.append([i,2*W/3])


# mixing gases
for m in range(40001):
    for n in range(1000):
        move()
    if m%400==0:
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)  # which color map looks better??
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
        plt.yticks((0,200,400),('0','200','400'),fontsize=14)
        plt.title('Mixing two gases',fontsize=22,fontweight='bold')
        plt.savefig('Tgas_mixing_step#'+str(m)+'e3.png')


