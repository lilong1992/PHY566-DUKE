# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 17:53:38 2016

@author: yanshen0
"""

import numpy as np
import pylab as plt
import random
import matplotlib.cm as cm


    

ni_shark = 150
ni_fish = 250

N = 80

T = 1000.0

fish_breed = 14
shark_breed = 19
shark_starve = 17


def period(x):
    if x < 0:
        x = N+x
    elif x > N-1:
        x = x-N
    return x    
    
global fish 
fish = np.empty((N,N))
global shark 
shark = np.empty((N,N))
fish.fill(-1)
shark.fill(-1)

global sharkstarve 
sharkstarve = np.zeros((N,N))


global fishmove 
fishmove = np.empty((N,N))
global sharkmove 
sharkmove = np.empty((N,N))
fishmove.fill(False)
sharkmove.fill(False)

a = random.sample(range(0,N**2), ni_shark+ni_fish)
#b = random.sample(range(0,N), ni_shark+ni_fish)
for i in range(ni_shark):
    shark[int(a[i]/N), a[i]-N*int(a[i]/N)] = 0
for i in range(ni_shark, ni_shark + ni_fish):
    fish[int(a[i]/N), a[i]-N*int(a[i]/N)] = 0


tank = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        if fish[i,j] != -1:
            tank[i,j] = 1
        if shark[i,j] != -1:
            tank[i,j] = -1
plt.figure()             #plot original distribution
fig = plt.imshow(tank, cmap=cm.seismic)
plt.show()           



#def fish_available(i,j):
#    a = []
#    if np.logical_and( fish[period(i-1),j] == -1 ,  shark[period(i-1),j] == -1):
#        a.append([period(i-1),j])
#    if np.logical_and( fish[period(i+1),j] == -1 ,  shark[period(i+1),j] == -1):
#        a.append([period(i+1),j])
#    if np.logical_and( fish[i ,period(j-1)] == -1 ,  shark[i,period(j-1)] == -1):
#        a.append([i,period(j-1)])
#    if np.logical_and( fish[i ,period(j+1)] == -1 ,  shark[i,period(j+1)] == -1):
#        a.append([i,period(j+1)])
#    return a
  
#print(fish[period(55),4])  
def fish_move():
    for i in range(N):       # this is the loop for x,y coordinate
        for j in range(N):   #
            if fish[i,j] != -1 and fishmove[i,j] == False:  #decide if there is a fish
                a = []
                if np.logical_and( fish[period(i-1),j] == -1 ,  shark[period(i-1),j] == -1):
                    a.append([period(i-1),j])
                if np.logical_and( fish[period(i+1),j] == -1 ,  shark[period(i+1),j] == -1):
                    a.append([period(i+1),j])
                if np.logical_and( fish[i ,period(j-1)] == -1 ,  shark[i,period(j-1)] == -1):
                    a.append([i,period(j-1)])
                if np.logical_and( fish[i ,period(j+1)] == -1 ,  shark[i,period(j+1)] == -1):
                    a.append([i,period(j+1)])
                                        # find movable spots, a is a list, a =((x1,y1), (x2,y2)...)
                if len(a) > 0:
                    r = random.sample(range(0,len(a)),1)  # randomly choose a coordinate from available ones
                    fish[a[ r[0] ][0],a[ r[0] ][1]] = fish[i,j]+1  #move fish
                    fishmove[a[ r[0] ][0],a[ r[0] ][1]] = True
                    if fish[a[ r[0] ][0],a[ r[0] ][1]] >= fish_breed: # decide give birth or not
                        fish[i,j] =0
                        fish[a[ r[0] ][0],a[ r[0] ][1]] = 0
                    else:
                        fish[i,j] = -1                
    fishmove.fill(False)          

#def shark_available(i,j):
#    a=[]
#    if fish(period(i-1),j) == -1 and fish(period(i+1),j) == -1 and fish(i,period(j-1)) == -1 and fish(i,period(j+1)) == -1
#          if shark(period(i-1),j) == -1:
#              a.append(period(i-1),j)
#          if shark(period(i+1),j) == -1:
#              a.append(period(i+1),j)
#          if shark(i,period(j-1)) == -1:
#              a.append(i,period(j-1))
#          if shark(i,period(j+1)) == -1:
#              a.append(i,period(j+1)) 
#    else:
#        if fish(period(i-1),j) != -1:
#            a.append(period(i-1),j)
#        if fish(period(i+1),j) != -1:
#            a.append(period(i+1),j)
#        if shark(i,period(j-1)) == -1:
#            a.append(i,period(j-1))
#        if shark(i,period(j+1)) == -1:
#            a.append(i,period(j+1))
#    return a
        
def shark_move():
    for i in range(N):       # this is the loop for x,y coordinate
        for j in range(N):
            if np.logical_and(shark[i,j] != -1 , sharkmove[i,j] == False): #if shark exist and not been moved
                a=[]                                #record available spots
                if fish[period(i-1),j] == -1 and fish[period(i+1),j] == -1 and fish[i,period(j-1)] == -1 and fish[i,period(j+1)] == -1: #if no fish to eat
                    if shark[period(i-1),j] == -1: 
                        a.append([period(i-1),j])
                    if shark[period(i+1),j] == -1:
                        a.append([period(i+1),j])
                    if shark[i,period(j-1)] == -1:
                        a.append([i,period(j-1)])
                    if shark[i,period(j+1)] == -1:
                        a.append([i,period(j+1)]) 
                    
                    if len(a) > 0: #if can move
                        r = random.sample(range(0,len(a)),1)
                        shark[a[ r[0] ][0],a[ r[0] ][1]] = shark[i,j]+1 #shark move, age +1
                        sharkstarve[a[ r[0] ][0],a[ r[0] ][1]] = sharkstarve[i,j]+1 #if shark cannot move, its starvation time won't grow...?
                        sharkstarve[i,j] = 0     #reset original starve time
                        if sharkstarve[a[ r[0] ][0],a[ r[0] ][1]] >= shark_starve: #if starve to death
                            shark[i,j] = -1    #die
                            shark[a[ r[0] ][0],a[ r[0] ][1]] = -1 #die
                        else: 
                            sharkmove[a[ r[0] ][0],a[ r[0] ][1]] = True #moved!!
                        
                        if shark[a[ r[0] ][0],a[ r[0] ][1]] >= shark_breed: # decide give birth or not
                            shark[i,j] =0        #baby shark
                            shark[a[ r[0] ][0],a[ r[0] ][1]] = 0 #new breeding cycle
                            sharkstarve[a[ r[0] ][0],a[ r[0] ][1]] = sharkstarve[i,j]+1
                            sharkstarve[i,j] = 0
                        else:
                            shark[i,j] = -1  #reset original spot
                    else:   #if cannot move, still starve, still die
                        sharkstarve[i,j] = sharkstarve[i,j]+1
                        if sharkstarve[i,j] >= shark_starve:
                            shark[i,j] = -1 
                else:   # fish to eat
                    if fish[period(i-1),j] != -1:
                        a.append([period(i-1),j])
                    if fish[period(i+1),j] != -1:
                        a.append([period(i+1),j])
                    if fish[i,period(j-1)] != -1:
                        a.append([i,period(j-1)])
                    if fish[i,period(j+1)] != -1:
                        a.append([i,period(j+1)])
                    
                    r = random.sample(range(0,len(a)),1) 
                    shark[a[ r[0] ][0],a[ r[0] ][1]] = shark[i,j]+1 #shark eat , age+1
                    fish[a[ r[0] ][0],a[ r[0] ][1]] = -1  # fish eaten
                    sharkstarve[a[ r[0] ][0],a[ r[0] ][1]] = 0 # feeling full!
                    sharkstarve[i,j] = 0         # no shark there
                    sharkmove[a[ r[0] ][0],a[ r[0] ][1]] = True # moved!!
                    if shark[a[ r[0] ][0],a[ r[0] ][1]] >= shark_breed: # decide give birth or not
                        shark[i,j] =0     #baby shark
                        shark[a[ r[0] ][0],a[ r[0] ][1]] = 0 #new breeding cycle
                    else:
                        shark[i,j] = -1  #reset original spot
    sharkmove.fill(False)            

time = np.linspace(0.0, T-1.0, int(T) )
fish_num = np.zeros(len(time))
shark_num = np.zeros(len(time))

for t in range(int(T)):
    fish_move()
    shark_move()
    for i in range(N):
        for j in range(N):
            if fish[i,j] != -1:
                fish_num[t] = fish_num[t]+1
            if shark[i,j] != -1:
                shark_num[t] = shark_num[t]+1
    


#plt.figure()             
#fig = plt.imshow(fish, cmap=cm.RdYlGn)
#plt.show()

#plt.figure()            
#fig = plt.imshow(shark, cmap=cm.RdYlGn)
#plt.show()


tank = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        if fish[i,j] != -1:
            tank[i,j] = 1
        if shark[i,j] != -1:
            tank[i,j] = -1
                  
plt.figure()             #plot original distribution
fig = plt.imshow(tank, cmap=cm.seismic)
plt.show()            


plt.figure() 
plt.plot(time, fish_num,'r', label = 'number of fish')
plt.plot(time, shark_num,'b', label = 'number of shark')
plt.legend(fontsize=12,loc='upper left')
plt.xlabel('time')
plt.grid()
plt.ylabel('population')
#plt.savefig('population.pdf')
plt.show()     

plt.figure() 
plt.plot(shark_num, fish_num,'r', label = 'phase diagram')
plt.legend(loc='upper right')
plt.xlabel('shark')
plt.ylabel('fish')
plt.grid()
#plt.savefig('phase.pdf')
plt.show() 







