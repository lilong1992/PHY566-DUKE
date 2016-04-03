import numpy as np
import random as rd
from matplotlib import pyplot as plt
from matplotlib import cm as cm

L = 100   # ocean dimension
T = 4000  # time period

Fish_Breed   = 15 # breed age
Shark_Breed  = 25 # breed age
Shark_Starve = 20 # starve age

n_Fish  = 2000 # fish number
n_Shark = 800  # shark number

# initialization at random
global Fish
global Shark
Fish = np.zeros((L,L))
Shark = np.zeros((L,L))
Fish.fill(-1)
Shark.fill(-1)

temp = rd.sample(range(0,L**2),n_Fish+n_Shark)
for i in range(n_Fish):
    Fish[int(temp[i])/L,int(temp[i])%L] = 0
for i in range(n_Fish,n_Fish+n_Shark):
    Shark[int(temp[i])/L,int(temp[i])%L] = 0

# last meal
global SharkStarve
SharkStarve = np.zeros((L,L))

# 0 if not moved; 1 if moved
global FishMove
global SharkMove
FishMove = np.zeros((L,L))
SharkMove = np.zeros((L,L))

def FishRun():
    global n_Fish
    for i in range(L):
        for j in range(L):
            if Fish[i,j] > -1 and FishMove[i,j] == 0:
                
                position = []
                if Fish[torus(i-1),j] == -1 and Shark[torus(i-1),j] == -1:
                    position.append([torus(i-1),j])
                if Fish[torus(i+1),j] == -1 and Shark[torus(i+1),j] == -1:
                    position.append([torus(i+1),j])
                if Fish[i,torus(j-1)] == -1 and Shark[i,torus(j-1)] == -1:
                    position.append([i,torus(j-1)])
                if Fish[i,torus(j+1)] == -1 and Shark[i,torus(j+1)] == -1:
                    position.append([i,torus(j+1)])

                if len(position) > 0:
                    pick = rd.randint(0,len(position)-1)
                    i_new = position[pick][0]
                    j_new = position[pick][1]
                    Fish[i_new,j_new] = Fish[i,j]+1  # move, increment age
                    FishMove[i_new,j_new] = 1
                    
                    if Fish[i_new,j_new] < Fish_Breed:  # cbeck breed
                        Fish[i,j] = -1
                    else:
                        Fish[i,j] = 0
                        Fish[i_new,j_new] = 0
                        n_Fish += 1
                else:
                    Fish[i,j] += 1  # stay, increment age
                        
    FishMove.fill(0)  # flush record

def SharkRun():
    global n_Fish
    global n_Shark
    for i in range(L):  # loop over ocean
        for j in range(L):
            if Shark[i,j] > -1 and SharkMove[i,j] == 0:
                meal = []  # find fish to eat
                if Fish[torus(i-1),j] > -1:
                    meal.append([torus(i-1),j])
                if Fish[torus(i+1),j] > -1:
                    meal.append([torus(i+1),j])
                if Fish[i,torus(j-1)] > -1:
                    meal.append([i,torus(j-1)])
                if Fish[i,torus(j+1)] > -1:
                    meal.append([i,torus(j+1)])
                
                if len(meal) > 0:
                    pick = rd.randint(0,len(meal)-1)
                    i_new = meal[pick][0]
                    j_new = meal[pick][1]
                    Shark[i_new,j_new] = Shark[i,j]+1  # move, increment age
                    SharkMove[i_new,j_new] = 1
                    Fish[i_new,j_new] = -1  # eat fish
                    n_Fish -= 1
                    SharkStarve[i_new,j_new] = 0
                    
                    if Shark[i_new,j_new] < Shark_Breed:  # cbeck breed
                        Shark[i,j] = -1
                    else:
                        Shark[i,j] = 0
                        SharkStarve[i,j] = 0
                        Shark[i_new,j_new] = 0
                        n_Shark += 1
                else:
                    position = []
                    if Shark[torus(i-1),j] == -1:
                        position.append([torus(i-1),j])
                    if Shark[torus(i+1),j] == -1:
                        position.append([torus(i+1),j])
                    if Shark[i,torus(j-1)] == -1:
                        position.append([i,torus(j-1)])
                    if Shark[i,torus(j+1)] == -1:
                        position.append([i,torus(j+1)])
                    
                    if len(position) > 0:
                        pick = rd.randint(0,len(position)-1)
                        i_new = position[pick][0]
                        j_new = position[pick][1]
                        Shark[i_new,j_new] = Shark[i,j]+1  # move, increment age
                        SharkMove[i_new,j_new] = 1
                        SharkStarve[i_new,j_new] = SharkStarve[i,j]+1
                        
                        if Shark[i_new,j_new] < Shark_Breed:  # cbeck breed
                            Shark[i,j] = -1
                        else:
                            Shark[i,j] = 0
                            Shark[i_new,j_new] = 0
                            n_Shark += 1

                        if SharkStarve[i_new,j_new] >= Shark_Starve:  # check sharve
                            Shark[i_new,j_new] = -1
                            n_Shark -= 1
                    else:
                        Shark[i,j] += 1  # stay, increment age
                        if SharkStarve[i,j] >= Shark_Starve:  # check sharve
                            Shark[i,j] = -1
                            n_Shark -= 1
                    
    SharkMove.fill(0)  # flush record

def torus(x):  # periodic boundary condition
    if x == L:
        x = 0
    if x == -1:
        x = L-1
    return x

def plot():  # plot current ocean
    Ocean = np.empty((L,L))
    Ocean.fill(0)
    for i in range(L):
        for j in range(L):
            if Fish[i,j] > -1:
                Ocean[i,j] = 1
            if Shark[i,j] > -1:
                Ocean[i,j] = -1
    plt.figure()
    plt.imshow(Ocean,cmap=cm.seismic)
    plt.xticks(())
    plt.yticks(())
    #plt.savefig('ocean.pdf')

time = np.linspace(0,T-1,T)
population = np.zeros((2,T))

for t in range(T):
    population[0,t] = n_Fish
    population[1,t] = n_Shark
    
    #plot()
    
    FishRun()
    SharkRun()

# plot population
plt.figure() 
plt.plot(time,population[0,:],'r',label='fish',linewidth=2)
plt.plot(time,population[1,:],'b',label='shark',linewidth=2)
plt.legend(fontsize=15,loc='upper right')
plt.xlabel('t',fontsize=15,fontweight='bold')
plt.ylabel('population',fontsize=15,fontweight='bold')
plt.xlim(0,T-1)
plt.ylim(0,L**2+100)
plt.grid()
#plt.savefig('population.pdf')
plt.show()

# plot phase diagram
plt.figure()
plt.plot(population[0,:],population[1,:],'r',label ='phase diagram',linewidth=2)
plt.legend(fontsize=15,loc='upper right')
plt.xlabel('shark',fontsize=15,fontweight='bold')
plt.ylabel('fish',fontsize=15,fontweight='bold')
plt.grid()
#plt.savefig('phase.pdf')
plt.show()
