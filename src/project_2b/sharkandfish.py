"""
Created on Sun Apr 03 21:14:59 2016

@author: lilon
"""

from pylab import *
import random as rd
L=160
W=50 #length and width of the ocean
nfish=3000 #number of initial fish
nsharks=300
fbreed=4 #fish breeding age
sbreed=10
sstarve=4 #shark starving age

fish=zeros((L,W)) #show where the fish is and its age
shark=zeros((L,W))
starve=zeros((L,W))
#initialize these three matrices
tmp=0
while tmp<nfish:
    i=rd.randint(0,L-1)
    j=rd.randint(0,W-1)
    if fish[i,j]==0: #0 means no fish
        fish[i,j]=rd.randint(1,fbreed) #give a random age
        tmp+=1

tmp=0
while tmp<nsharks:
    i=rd.randint(0,L-1)
    j=rd.randint(0,W-1)
    if shark[i,j]==0:
        shark[i,j]=rd.randint(1,sbreed)
        starve[i,j]=1
        tmp+=1
#finish initialization
def move():
    global fish,shark,starve,nsharks,nfish
    #fish moves first
    tmp=copy(fish) #tmp is used to keep track of each fish, it's fixed in each move function
    for i in range(L):
        for j in range(W):
            if tmp[i,j]!=0:#it's fish
                inew,jnew=checkandgetrandomdirection_fish(i,j)
                if inew==-1:
                    fish[i,j]+=1 #cannot move increase one year
                else:
                    fish[i,j]+=1
                    if fish[i,j]>fbreed:
                        fish[inew,jnew]=1
                        fish[i,j]=1
                        nfish+=1
                    else:
                        fish[inew,jnew]=fish[i,j]
                        fish[i,j]=0
                        
    #sharks move next
    tmp=copy(shark)
    for i in range(L):
        for j in range(W):
            if tmp[i,j]>0:#it's a shark
                inew,jnew=checkandgetrandomdirection_stof(i,j)
                if inew==-1: #no fish around
                    if starve[i,j]>sstarve:#starvation delete the shark
                        shark[i,j]=0
                        starve[i,j]=0
                        nsharks-=1
                    else:
                        inew,jnew=checkandgetrandomdirection_shark(i,j)#random move
                        if inew==-1:
                            shark[i,j]+=1
                            starve[i,j]+=1
                        else:
                            shark[i,j]+=1
                            starve[inew,jnew]=starve[i,j]+1
                            if shark[i,j]>sbreed: #check if it can breed
                                shark[inew,jnew]=1
                                shark[i,j]=1
                                starve[i,j]=1
                                nsharks+=1
                            else:
                                shark[inew,jnew]=shark[i,j]
                                shark[i,j]=0
                                starve[i,j]=0                           
                else:#go for fish
                    fish[inew,jnew]=0 #eat it!
                    nfish-=1
                    shark[i,j]+=1
                    starve[inew,jnew]=1
                    if shark[i,j]>sbreed:#check if it can breed
                        shark[inew,jnew]=1
                        shark[i,j]=1
                        starve[i,j]=1
                        nsharks+=1
                    else:
                        shark[inew,jnew]=shark[i,j]
                        shark[i,j]=0
                        starve[i,j]=0
                            
def checkandgetrandomdirection_fish(i,j):
    global fish,shark
    direc=[]
    if fish[(i-1)%L,j]==0 and shark[(i-1)%L,j]==0: #left, avoid sharks and fish
        direc.append([(i-1)%L,j])
    if fish[(i+1)%L,j]==0 and shark[(i+1)%L,j]==0: #right
        direc.append([(i+1)%L,j])
    if fish[i,(j-1)%W]==0 and shark[i,(j-1)%W]==0: #down
        direc.append([i,(j-1)%W])
    if fish[i,(j+1)%W]==0 and shark[i,(j+1)%W]==0: #up
        direc.append([i,(j+1)%W])
    if direc==[]:
        return -1,-1
    else:
        newposition=direc[rd.randint(0,len(direc)-1)]
        return newposition[0],newposition[1]
        
def checkandgetrandomdirection_stof(i,j):
    global fish
    direc=[]
    if fish[(i-1)%L,j]>0: #left
        direc.append([(i-1)%L,j])
    if fish[(i+1)%L,j]>0: #right
        direc.append([(i+1)%L,j])
    if fish[i,(j-1)%W]>0: #down
        direc.append([i,(j-1)%W])
    if fish[i,(j+1)%W]>0: #up
        direc.append([i,(j+1)%W])
        """
    if fish[(i-1)%L,(j-1)%W]>0:#down left
        direc.append([(i-1)%L,(j-1)%W])
    if fish[(i-1)%L,(j+1)%W]>0:
        direc.append([(i-1)%L,(j+1)%W])
    if fish[(i+1)%L,(j-1)%W]>0:
        direc.append([(i+1)%L,(j-1)%W])
    if fish[(i+1)%L,(j+1)%W]>0:
        direc.append([(i+1)%L,(j+1)%W])
        """
    if direc==[]:
        return -1,-1
    else:
        newposition=direc[rd.randint(0,len(direc)-1)]
        return newposition[0],newposition[1]
        
def checkandgetrandomdirection_shark(i,j):
    global shark
    direc=[]
    if shark[(i-1)%L,j]==0: #left
        direc.append([(i-1)%L,j])
    if shark[(i+1)%L,j]==0: #right
        direc.append([(i+1)%L,j])
    if shark[i,(j-1)%W]==0: #down
        direc.append([i,(j-1)%W])
    if shark[i,(j+1)%W]==0: #up
        direc.append([i,(j+1)%W])
    if direc==[]:
        return -1,-1
    else:
        newposition=direc[rd.randint(0,len(direc)-1)]
        return newposition[0],newposition[1]
                    
#start simulation
T=1000
time = np.linspace(0,T-1,T)
population = np.zeros((T,2))
for t in range(T):
    population[t,0]=nfish
    population[t,1]=nsharks
    move()

figure() 
plot(time,population[:,0],'r',label='fish',linewidth=2)
plot(time,population[:,1],'b',label='shark',linewidth=2)
legend(fontsize=15,loc='upper right')
xlabel('t',fontsize=15,fontweight='bold')
ylabel('population',fontsize=15,fontweight='bold')
grid()
show()                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                