'''
Created on Apr 6, 2016

@author: Chris
'''

import numpy as np
import matplotlib.pyplot as plt
import random as rn
import matplotlib.cm as cm


#Define some useful Constants
#the width of a square array world...
N = 100 #will make a 40x40 Grid
numFish = 4000 #starting number of fishies
numShark = 50 #starting number of sharks
starveSteps = 10 #how many steps does a shark go without eating before it dies... 
breedSteps = 15 #how many steps does a shark go before it breeds
ocean = np.zeros((N,N)) #define an empty ocean grid! - try making it a two D list so its hashable? [[]]?
values = dict() #pretty sure this makes an empty dictionary...
global sharkcounter
global fishcounter
 #initialize the counters...
sharkcounter = numShark
fishcounter = numFish
iterations = 1000




def initialize():
    #this function will cause the initialization of the griddy grid Grid
    #note: this method currently can overwrite fish with sharks.
    for i in range (0, numFish-1):
        #populate the grid with the fishies...
        #generate two random numbers
        X = rn.randint(0,N-1)
        Y = rn.randint(0,N-1) #make a rnadom coordinate pair within the grid
        ocean[X][Y] = -1 #-1 will correspond to lil fishers is tihs X Y assignment reasonable? 
        
    for j in range (0, numShark-1):
        #populate the grid with the fishies...
        #generate two random numbers
        X = rn.randint(0,N-1)
        Y = rn.randint(0,N-1) #make a rnadom coordinate pair within the grid
        ocean[X][Y] = 1 #-1 will correspond to lil fishers
        
    #this initializes the dictionary that we use the reference stuff
    for x in range(N):
        for y in range(N): #can I just make a new entry for this values here?
            values[(x,y)] = [ocean[x][y], 0, 0] #each location corresponds to an array that has (gridvalue, stepsSinceEat, stepsTotal) 
            #key tuple value lisT??
            
        

def fishMove(location):
    #pull the location for a fishy mcfisherston - should already know that value = -1
    availables = [] #MADE EMPTY LIST TO AVOID SIZE ASSIGNMENT
    x = location[0]
    y = location[1] #this should take care of the algebras
    
    
    #THESE CONDITIONS ARE INSUFFICIENT
    addx = 0
    addy = 0 #added on in the case we are at zero
    
    if (x == 0):
        addx = N
    if (y == 0):
        addy = N
    #if either of these are triggered, the -1 checks will map to N-1, aka the other side of the grid
    
    xs = [x-1+addx, x, x, (x+1)%(N)] #modding by (N-1) should account for trying to access the distant boundaries... NOT SUFFICIENT!!!!
    ys = [y, (y+1)%(N), y-1+addy, y] #define some lists of appropriate moving locations... 
    for test in range(0,3):
        if (ocean[xs[test]][ys[test]] == 0): #if this location is zero add it to available...
            availables.append((xs[test], ys[test])) #adds the empty location to availables... CHANGED TO TUPLE
    
    if (len(availables) != 0): #if there are available locations    
        index = rn.randint(0, len(availables)-1) #grab a random appropriate index and that's where we move...
        newx = availables[index][0]
        newy = availables[index][1]
        ocean[x][y] = 0 #can I do this? leave the empty space...
        ocean[newx][newy] = -1 # --- availables[index] should be the randomly chosen TUPLE so availables[index][0] should be x... etc
        
        tempArray = values.get((x,y))#trying this...
        values[(newx,newy)] = tempArray #this requires no updating because fish dont eat or starve in this ecosystem... CHANGED TO TUPLEs
        values[(x,y)] = [0, 0, 0] #this should reset the value in the map to an empty spot...
     
def sharkMove(location):
    #pull the location for a shark - should already know that value = 1
    global fishcounter
    global sharkcounter
    favailables = [] #np.empty() #possible locations, do I need to assign size?
    availables = [] #np.empty()
    x = location[0]
    y = location[1] #this should take care of the algebras
    move = False
    
    
    ##################CONDITIONS TO AVOID OUT OF BOUNDS##################################
    addx = 0
    addy = 0 #added on in the case we are at zero
    if (x == 0):
        addx = N
    if (y == 0):
        addy = N
    #these conditionals should map 40 to 0, -1 to 39 etc
    
    xs = [x-1+addx, x, x, (x+1)%N] #NEED TO IMPOSE MODULARITY CONDITION FOR THESE TO WORK
    ys = [y, (y+1)%N, y-1+addy, y] #define some lists of appropriate moving locations... 
    
    
    ####################GATHER DATA ON NEIGHBOR SITES###################################
    for test in range(0,3): #this might need to go to 4 if its exclusive 
        if (ocean[xs[test]][ys[test]] == -1): #if this location is A FISH next to it we add......
            favailables.append([xs[test], ys[test]]) #adds the empty location to availables...
        if (ocean[xs[test]][ys[test]] == 0): #if this location is EMPTY next to it we add......
            availables.append([xs[test], ys[test]]) #adds the empty location to availables... #PROBLEM ---- availables[test] will EASILY index out here... we need add..
        
    #################IF THERE IS AN ADJACENT FISH - MOVE THERE AND EAT IT ################################
    if (len(favailables) != 0): #if there is an adjacent fishy fisher we go there...    
        index = rn.randint(0, len(favailables)-1) #grab a random appropriate index and that's where we move...
        newx = favailables[index][0]
        newy = favailables[index][1]
        
        ocean[x][y] = 0 #can I do this? leave the empty space...
        ocean[newx][newy] = 1 #this is where the SHARK is now
        move = True
        #if htis has been triggered, the shark has now eaten so we must update the number of steps since eaten...
        tempArray = values.get((x,y)) #CHANGED TO TUPLE
        tempArray[1] = 0 #SET THE STEPS SINCE LAST EATEN TO ZERO
        tempArray[2] += 1 #INCREMENT THE TOTAL STEPS BY ONE
        values[(newx,newy)] = tempArray #assign the new array to the new location - CHANGED TO TUPLE
        values[(x,y)] = [0, 0, 0] #this should reset the value in the map to an empty spot... CHANGED TO TUPLE
        #removed get calls here
        #SINCE A FISHY HAS BEEN EATEN
        fishcounter = fishcounter - 1 #reduce fishcounter 

##########IF THERE ARE NO ADJACENT FISH BUT THERE IS AN EMPTY SPOT, MOVE THERE#################################
    elif (len(availables) != 0): #if there are no fishy spots, and there ARE available empty spots, we try that one...
        index = rn.randint(0, len(availables)-1) #grab a random appropriate index and that's where we move...
        newx = availables[index][0]
        newy = availables[index][1]
        ocean[x][y] = 0 #can I do this? leave the empty space...
        ocean[newx][newy] = 1 #this is where the SHARK is now
        
        tempArray = values.get((x,y))
        tempArray[1] += 1 #INCREMENT THE STEPS SINCE EATEN
        tempArray[2] += 1 #INCREMENT THE TOTAL STEPS BY ONE
        values[(newx,newy)] = tempArray #assign the new array to the new location
        values[(x,y)] = (0, 0, 0) #this should reset the value in the map to an empty spot...
        #removed get calls here too...
        move = True
        
        
#################### IF THERE ARE NO AVAILABLE NEIGHBORING SPOTS WE STAY PUT########################
    elif (len(availables) == 0 and len(favailables) == 0): #check if there REALLY is no place to go... we have to increment the steps anyway, unlike with fish
        tempArray = values.get((x,y))
        tempArray[1] += 1 #INCREMENT THE STEPS SINCE EATEN
        tempArray[2] += 1 #INCREMENT THE TOTAL STEPS BY ONE
        values[(x,y)] = tempArray #this should assign the NEWLY INCREMENTED ARRAAY to the ORIGINAL location...
        #removed get call
        move = False 
        
# THIS IS WRONG - WE ARE LOOKING AT TEMP ARRAY FOR THE ORIGINAL LOCATION BUT MIGHT HAVE MOVED! #####

    #tempArray = values.get((x,y)) #brax to parens
    #if (tempArray[1] > starveSteps): #CHECK TIMESTEPS SINCE EATING
    
    if (move == False): #if we didnt move
        tempArray = values.get((x,y)) #temp array should be the ORIGINAL location\
        if (tempArray[1] > starveSteps): #if the second value aka the steps since eaten is greater than starve steps...    
            values[(x,y)] = [0,0,0] #set this to an EMPTY LOCATION!!! - removed get call
            ocean[x][y] = 0 #reset the grid location?
            sharkcounter -= 1 #reduce the memoized number of sharks in the setup...
            
    #Now if we DID move...
    elif (move == True): #if the shark has moved but still needs to starve... should be at index[0], index[1] now
        tempArray = values.get((newx,newy)) #temp array should be the NEW location\
        if (tempArray[1] > starveSteps):
            values[(newx,newy)] = [0,0,0] #set this to an EMPTY LOCATION!!! - could this throw an error since newx etc might not be initialized? - removed get call
            ocean[newx][newy] = 0 #reset the grid location?
            sharkcounter -= 1 #reduce the memoized number of sharks in the setup...

    #interesting... temp array is already defined so this call should work now...
    if (tempArray[2] > breedSteps): #JUST REALIZED THEY CAN ONLY BREED IF THEY MOVED OTHERWISE HTERE IS NO SPACE!!! THEREFORE JUST ADD A NEW SHARK TO THE PREVIOUS LOC
        ocean[x][y] = 1 #reset the grid location?
        values[(x,y)] = [1,0,0] #set this to NEW SHARK!!!!!! - removed get call
        sharkcounter += 1 #reduce the memoized number of sharks in the setup...
        #NEED TO RESET THE BREEDING
        tempArray2 = values.get((newx, newy)) #this is the new location of the shark that just made a baby
        tempArray2[2] = 0
        values[(newx,newy)] = tempArray2 #reassign the new array with the final breed step counter reset to zero...     
        

#CORE#
initialize() #prepares the grid
for z in range(iterations):
    for q in range(N):
        for w in range(N): #THIS MIGHT BE EXCLUSIVE??
            #should go through the whole grid "iterations" number of times
            if (ocean[q][w] == -1): #perhaps these are not getting called!
                fishMove((q,w)) #make a call to fish move...
            if (ocean[q][w] == 1):
                sharkMove((q,w)) #CHANGED INPUT ARGS TO TUPLES
    
    if (z%50==0): #every 100 grids computed...
        plt.figure()            
        fig = plt.imshow(ocean, cmap=cm.RdYlGn)
        print(fishcounter)
        print(sharkcounter)
        plt.show()
    
            
        
        


        

           
    
    