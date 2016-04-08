'''
Created on Apr 6, 2016

@author: Chris
'''

import numpy as np
import matplotlib.pyplot as plt
import random as rn
import matplotlib.cm as cm
import matplotlib.animation as animation


#the width of a square array world...
N = 100 #will make grid

numFish = 1000 #starting number of fishies
numShark = 25 #starting number of sharks
starveSteps = 10 #how many steps does a shark go without eating before it dies... 
breedSteps = 15 #how many steps does a shark go before it breeds
fbreedSteps = 15 #how many steps does a fish go before it breeds
ocean = np.zeros((N,N)) #define an empty ocean grid!
values = dict() #Make an empty dictionary - will have a location (x,y) tuple correspond to a list of [species, steps since eat, steps since breed] 
global sharkcounter #counting varibales
global fishcounter

 #initialize the counters...
sharkcounter = numShark
fishcounter = numFish
iterations = 1000 #set the number of iterations, as in full grids evaluated 




def initialize():
    #this function will cause the initialization of the ocean
    #note: this method currently can overwrite fish with sharks - a potential change for another time
    for i in range (0, numFish-1):
        #populate the grid with the fishies...
        #generate two random numbers
        X = rn.randint(0,N-1)
        Y = rn.randint(0,N-1) #make a random coordinate pair within the grid
        ocean[X][Y] = -1 #-1 will correspond to lil fishers is tihs X Y assignment reasonable? 
        
    for j in range (0, numShark-1):
        #populate the grid with the fishies...
        #generate two random numbers
        X = rn.randint(0,N-1)
        Y = rn.randint(0,N-1) #make a random coordinate pair within the grid
        ocean[X][Y] = 1 #-1 will correspond to lil fishers
        
    #this initializes the dictionary that we use the reference stuff
    for x in range(N):
        for y in range(N): #can I just make a new entry for this values here?
            values[(x,y)] = [ocean[x][y], 0, 0] #each location corresponds to an array that has (species, stepsSinceEat, stepsTotal) 
            #key tuple value list
            
        

def fishMove(location):
    global fishcounter
    #pull the location for a fishy - should already know that value = -1
    availables = [] #holds locations
    x = location[0]
    y = location[1] #input is a tuple
    
    
    addx = 0
    addy = 0 #added on in the case we are at zero
    
    if (x == 0):
        addx = N
    if (y == 0):
        addy = N
    #if either of these are triggered, the -1 checks will map to N-1, aka the other side of the grid
    
    xs = [x-1+addx, x, x, (x+1)%(N)] #modding by (N-1) should account for trying to access the distant boundaries... 
    ys = [y, (y+1)%(N), y-1+addy, y] #define some lists of appropriate moving locations... 
    
    for test in range(0,4): #check neighbor sites
        if (ocean[xs[test]][ys[test]] == 0): #if this location is zero add it to available...
            availables.append((xs[test], ys[test])) #adds the empty location to availables... 
    
    if (len(availables) != 0): #if there are available locations    
        index = rn.randint(0, len(availables)-1) #grab a random appropriate index and that's where we move...
        newx = availables[index][0]
        newy = availables[index][1]
        ocean[x][y] = 0 #leave the space empty...
        ocean[newx][newy] = -1 #new fish location in grid
        
        tempArray = values.get((x,y))#updating dictionary values.
        tempArray[2] += 1 #increment the steps since breeding by one...
        values[(newx,newy)] = tempArray #update dict
        values[(x,y)] = [0, 0, 0] #this should reset the value in the map to an empty spot...
        
        
        #wait I need to reset steps since breeding too...
        #if we have a movement, we have the potential to make a lil baby fishy 
        if (tempArray[2] > fbreedSteps): #if it is time to make lil fish
            
            #new code
            tempArray = values.get((newx, newy))
            tempArray[2] = 0 #RESET THE NEW LOCATIONS STEPS SINCE BREEDING...
            values[(newx,newy)] = tempArray
            #end new code
            
            values[(x,y)] = [-1, 0, 0] #make new baby fish in the dict! 
            ocean[x][y] = -1 #set new fish values for the spot we just moved from.
            fishcounter += 1  #increment the memoized fishcounter variable
        
    elif (len(availables) == 0): #gets hit if the guy doesnt move... needs to update the steps since breed again
        tempArray = values.get((x,y))
        tempArray[2] += 1 
        values[(x,y)] = tempArray #simply updates the values entry to increment the final entry by one meaning
        #HOWEVER, if this is getting incremented we do not need to check if it is time to breed, because no movement means no neighboring spots anyway! 
        
     
def sharkMove(location):
    #pull the location for a shark - should already know that value = 1
    global fishcounter
    global sharkcounter
    favailables = [] #will hold fish locations
    availables = [] #will hold empty locations
    x = location[0]
    y = location[1] #input is a tuple
    move = False
    #should be unnecessary but here's a initialization
    newx = x
    newy = y
    
    ##################CONDITIONS TO AVOID OUT OF BOUNDS##################################
    addx = 0
    addy = 0 #added on in the case we are at zero
    if (x == 0):
        addx = N
    if (y == 0):
        addy = N
    #these conditionals should map N to 0, -1 to N-1 etc
    
    xs = [x-1+addx, x, x, (x+1)%N] 
    ys = [y, (y+1)%N, y-1+addy, y]  
    
    
    ####################GATHER DATA ON NEIGHBOR SITES###################################
    for test in range(0,4): #access neighboring locations
        if (ocean[xs[test]][ys[test]] == -1): #if this location is A FISH next to it we add......
            favailables.append([xs[test], ys[test]]) #adds the empty location to favailables...
        if (ocean[xs[test]][ys[test]] == 0): #if this location is EMPTY next to it we add......
            availables.append([xs[test], ys[test]]) #adds the empty location to availables... 
        
    #################IF THERE IS AN ADJACENT FISH - MOVE THERE AND EAT IT ################################
    if (len(favailables) != 0): #if there is an adjacent fishy fisher we go there...    
        index = rn.randint(0, len(favailables)-1) #grab a random appropriate index and that's where we move...
        newx = favailables[index][0]
        newy = favailables[index][1]
        
        ocean[x][y] = 0 #leave the empty space...
        ocean[newx][newy] = 1 #this is where the SHARK is now
        move = True
        #if htis has been triggered, the shark has now eaten so we must update the number of steps since eaten...
        tempArray = values.get((x,y)) #update dict values
        tempArray[1] = 0 #SET THE STEPS SINCE LAST EATEN TO ZERO
        tempArray[2] += 1 #INCREMENT THE TOTAL STEPS BY ONE
        values[(newx,newy)] = tempArray #assign the new array to the new location 
        values[(x,y)] = [0, 0, 0] #this should reset the value in the map to an empty spot... 

        #SINCE A FISHY HAS BEEN EATEN
        fishcounter = fishcounter - 1 #reduce fishcounter 

##########IF THERE ARE NO ADJACENT FISH BUT THERE IS AN EMPTY SPOT, MOVE THERE#################################
    elif (len(availables) != 0): #if there are no fishy spots, and there ARE available empty spots, we try that one...
        index = rn.randint(0, len(availables)-1) #grab a random appropriate index and that's where we move...
        newx = availables[index][0]
        newy = availables[index][1]
        ocean[x][y] = 0 # leave the empty space...
        ocean[newx][newy] = 1 #this is where the SHARK is now
        
        tempArray = values.get((x,y))
        tempArray[1] += 1 #INCREMENT THE STEPS SINCE EATEN
        tempArray[2] += 1 #INCREMENT THE TOTAL STEPS BY ONE
        values[(newx,newy)] = tempArray #assign the new array to the new location
        values[(x,y)] = (0, 0, 0) #this should reset the value in the map to an empty spot...

        move = True
        
        
#################### IF THERE ARE NO AVAILABLE NEIGHBORING SPOTS WE STAY PUT########################
    elif (len(availables) == 0 and len(favailables) == 0): #check if there REALLY is no place to go... we have to increment the steps
        tempArray = values.get((x,y))
        tempArray[1] += 1 #INCREMENT THE STEPS SINCE EATEN
        tempArray[2] += 1 #INCREMENT THE TOTAL STEPS BY ONE
        values[(x,y)] = tempArray #this should assign the NEWLY INCREMENTED ARRAY to the ORIGINAL location...

        move = False 
        

    
    if (move == False): #if we didnt move
        tempArray = values.get((x,y)) #temp array should be the ORIGINAL location
        if (tempArray[1] > starveSteps): #if the second value aka the steps since eaten is greater than starve steps...    
            values[(x,y)] = [0,0,0] #set this to an EMPTY LOCATION!!!
            ocean[x][y] = 0 #reset the grid location
            sharkcounter -= 1 #reduce the memoized number of sharks in the setup...
            
    #Now if we DID move...
    elif (move == True): #if the shark has moved but still needs to starve... should be at index[0], index[1] now
        tempArray = values.get((newx,newy)) #temp array should be the NEW location\
        if (tempArray[1] > starveSteps):
            values[(newx,newy)] = [0,0,0] #set this to an EMPTY LOCATION!!! - 
            ocean[newx][newy] = 0 #reset the grid location
            sharkcounter -= 1 #reduce the memoized number of sharks in the setup...

    #temp array is already defined so this call should work now...
    if (tempArray[2] > breedSteps): #THEY CAN ONLY BREED IF THEY MOVED OTHERWISE HTERE IS NO SPACE!!! THEREFORE JUST ADD A NEW SHARK TO THE PREVIOUS LOC
        ocean[x][y] = 1 #reset the grid location
        values[(x,y)] = [1,0,0] #set this to NEW SHARK!
        sharkcounter += 1 #reduce the memoized number of sharks in the setup...
        #NEED TO RESET THE BREEDING
        tempArray2 = values.get((newx, newy)) #this is the new location of the shark that just made a baby
        tempArray2[2] = 0
        values[(newx,newy)] = tempArray2 #reassign the new array with the final breed step counter reset to zero...     
        




#CORE#
initialize() #prepares the grid
sharkpop = []
fishpop = []
timesteps = []
time = 0 


#oceanHolder = [] 

for z in range(iterations):
    for q in range(N):
        for w in range(N): 
            #should go through the whole grid "iterations" number of times
            if (ocean[q][w] == -1): 
                fishMove((q,w)) #make a call to fish move...
            if (ocean[q][w] == 1):
                sharkMove((q,w)) #call sharkmove
    
    sharkpop.append(sharkcounter)
    fishpop.append(fishcounter)
    timesteps.append(time)
    time += 1
    
    
   # oceanHolder.append(ocean) #append the most recent ocean to the list that holds all the oceans for animation...
    if (z%100==0): #every 100 grids computed...
        plt.figure()            
        fig = plt.imshow(ocean, cmap=cm.RdYlGn)
        print(fishcounter)
        print(sharkcounter)
        plt.show()
        
        
        
#failed animation code
# fig, ax = plt.subplots()
# global iter
# 
# iter = 0
# 
# def grabGrid(dummy):
#     global iter 
#     iter += 1
#     return oceanHolder[iter]
# 
# #ani = animation.FuncAnimation(fig, grabGrid, np.arange(1, iterations)) #is this gonna work? I didnt really define fig...
# anim = animation.FuncAnimation(fig, grabGrid, init_func=None,
#                                frames=iterations, interval=1, blit=True)
# plt.show()

            
plt.plot(timesteps, sharkpop, label='SharkPopulation')    
plt.plot(timesteps, fishpop, label='FishPopulation') 
plt.ylabel("Population")
plt.xlabel("Timesteps")
plt.title("Shark and Fish Populations over 1000 timesteps")    
plt.legend()
plt.show()   
    
        


        

           
    
    