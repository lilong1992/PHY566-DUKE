'''
Created on Mar 24, 2016

@author: Chris
'''
import numpy as np
import random as rd
import pylab as plt
import matplotlib.cm as cm

H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
availDict = {} #define new dictionary

particleSet = set() #define an empty set that will hold the location of all particles...
mobileSet = set() #define an empty set that will hold locations of all particles that have empty spots near them. 


def move(y,x):
    destination = getAvail(y,x) #the destination tuple is retrieved
    xnew = destination[1]
    ynew = destination[0] #grab x and y 
    particleSet.add((ynew,xnew)) #add the new particles location to this set
    particleSet.remove((y,x)) #take the particle out of hte last one where it came from - why did this throw a key error???
    u[ynew, xnew] = u[y,x] #SET THE NEW SPOT EQUAL TO THE OLD SPOT
    u[y,x] = 0 #set the original spot to empty...

def updateAvails(y,x): #the input is an x,y tuple
    #this is a method that will update the available sites around a location
    availDict[(y,x)] = [] #set the corresponding VALUE for KEY tuple (x,y) equal to an EMPTY list of TUPLES
    isMobile = False
    if (u[y+1,x] == 0): #if the space is unoccupied... INDEXING OUT OF BOUNDS
        availDict[(y,x)].append((y+1,x)) #the TUPLE (x+1,y) is APPENDED to the empty list that corresponds to location (x,y)
        mobileSet.add((y,x))
        isMobile = True
    if (u[y-1,x] == 0): #if the space is unoccupied...
        availDict[(y,x)].append((y-1,x))    
        mobileSet.add((y,x))
        isMobile = True
    if (u[y,x+1] == 0): #if the space is unoccupied...
        availDict[(y,x)].append((y,x+1))
        mobileSet.add((y,x))
        isMobile = True
    if (u[y,x-1] == 0): #if the space is unoccupied...
        availDict[(y,x)].append((y,x-1))
        mobileSet.add((y,x)) #holds no duplicates so it doesnt matter if we add it several times...
        isMobile = True
        
    if (isMobile == False and ((y,x) in mobileSet)): #if it was mobile before and no longer is... take it out of the mobile set!
        mobileSet.remove((y,x))
        

def getAvail(y,x):
    #this function gets an available site for location x,y
    updateAvails(y,x) 
    tempList = availDict[(y,x)]
    length = len(tempList) #number of available sites.. 0 to 4
    if (length != 0):
        #if there are available sites
        index = rd.randint(0,length-1) #think this ought to be -1
        site = tempList[index] #this should give the element in the available dictionary corresponding to to (x,y) at position index...
        return site #RETURNS A TUPLE
    return (y,x) #returns the original site if there are no available sites...

# initialize u, particleSet and mobileSet
u = np.zeros((H+1,W+1)) #should stop it from out of boundsing...might still need -1!
print("initializing...")
for i in range(H-1):
    for j in range(int(W/3)): #added int call #I got rid of the 1, stuff cuz I think that was not necessary and making the edges diffuse
        u[i,j] = -1
        particleSet.add((i,j)) #is this syntax ok
    for j in range(2*int(W/3),W): #added int call
        u[i,j] = 1
        particleSet.add((i,j)) #is this syntax ok
#once the particles are in place...

#initialize mobileSet
for i in range(H-1):
    for j in range(W-1): #this isn't the most efficient but only gets called once so whatever.
        updateAvails(i,j) #update this particles avails
        if (getAvail(i,j) != (i,j) and u[i,j] != 0 and j != 1 and j!= 598): #if there is an available spot, AND a particle and it's not sitting on the boundary 
            mobileSet.add((i,j))
print("sets initialized")     
        
        
# mixing gases
for m in range(10001):
    print("m is " + str(m))
    for n in range(100): #decreased these because my computer probably wont make it...
        test = rd.sample(particleSet.intersection(mobileSet), 1) #grab a random PARTICLE that is classified as MOBILE and MOVE IT
        h = test[0][0]
        w = test[0][1] 
        move(h,w)
        for i in range(h-2,h+2):
            for j in range(w-2, w+2):
                if(i<398 and i>2 and j<598 and j>2): #should stop this from indexing out of bounds BUT will screw up the edge cases ... to fix later
                    updateAvails(i,j) #this should update every square within two spaces so that the sites stay accurate
        
    if m%100 == 0:  # output every 100 outer steps
        print('iteration number: ',m,'x 10e6')
        plt.figure()
        plt.imshow(u, cmap=cm.Spectral)
        plt.xlabel('x',fontsize=20,fontweight='bold')
        plt.ylabel('y',fontsize=20,fontweight='bold')
        plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
        plt.yticks((0,200,400),('0','200','400'),fontsize=14)
        plt.title('Mixing two gases - Dict Method + m =' + str(m),fontsize=22,fontweight='bold')
        plt.savefig('new trial gases_'+str(m)+'.pdf')  # name each figure with index
        #plt.show()         
        
        

