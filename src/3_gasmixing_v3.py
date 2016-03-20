"""
modified from v2 by Long Li
seems like it's slower 
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


def move(): #pick one particle and move one step
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,len(available)-1)
    i = available[pick][0]
    j = available[pick][1]
    moved=False
    dice=rd.random() #direction
    if dice < 0.25: #left
        if j-1>=0 and u[i,j-1]==0:#check if it's allowed to be moved in
            u[i,j-1]=u[i,j]
            u[i,j]=0
            moved=True
    elif dice<0.5: #right
        if j+1<W and u[i,j+1]==0:
            u[i,j+1]=u[i,j]
            u[i,j]=0
            moved=True
    elif dice<0.75: #down
        if i-1>=0 and u[i-1,j]==0:
            u[i-1,j]=u[i,j]
            u[i,j]=0
            moved=True
    else: #up
        if i+1<H and u[i+1,j]==0:
            u[i+1,j]=u[i,j]
            u[i,j]=0
            moved=True
    if moved:
        available.remove([i,j]) #i,j is no longer a particle
        add_new_avaliablesite(i,j) #add new particles that can move


# initialize u
H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
u = np.zeros((H,W))
for i in range(H):
    for j in range(W/3):
        u[i,j] = -1
    for j in range(W/3,2*W/3):
        u[i,j] = 0
    for j in range(2*W/3,W):
        u[i,j] = 1

# initialize available sites

available = []
for i in range(H):
    available.append([i,W/3-1])  # available sites at the beginning
    available.append([i,2*W/3])


# mixing gases
for m in range(10001):
    for n in range(10000):
        move()
    if m%50==0:
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)  # which color map looks better??
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
        plt.yticks((0,200,400),('0','200','400'),fontsize=14)
        plt.title('Mixing two gases',fontsize=22,fontweight='bold')
        plt.savefig('gas_mixing_step#'+str(m)+'e4.png')

