
"""
Created on Tue Mar 15 15:47:54 2016

@author: yanshen0
"""

from pylab import *
from numpy import *


time = linspace(4,100,97) #time array, from 4 to 100
xaverage = zeros(97)       #average of x over 1e4 random walks
xsquare_ave = zeros(97)    #average of x^2 over 1e4 random walks
rsquare_ave = zeros(97)    #average of r^2 over 1e4 random walks
 
for i in range(len(time)):
    n = time[i]       
    k = 0.0       #track No. of random walks
    while k < 1e4:
        x = 0
        y = 0     #starting from (0,0)
        for j in range(int(n)):   
           rand = random.uniform(0.0,1.0)
           if rand <= 0.25:
               y = y + 1
           elif rand>0.25 and rand<=0.5:
               y = y - 1
           elif rand>0.5 and rand<=0.75:
               x = x - 1
           else:
               x = x + 1
        xaverage[i] = xaverage[i] + x
        xsquare_ave[i] = xsquare_ave[i] + x**2
        rsquare_ave[i] = rsquare_ave[i] + x**2 + y**2
        k = k+1.0
    xaverage[i] = xaverage[i]/k
    xsquare_ave[i] = xsquare_ave[i]/k
    rsquare_ave[i] = rsquare_ave[i]/k 

#plot x average    
figure()
plot(time, xaverage,'k', label = '<xn>')
legend(loc='upper left')
xlabel('time step')
grid()
ylabel('x average')
#savefig('xaverage.pdf')
show()  

#plot x^2 average
figure()
plot(time, xsquare_ave,'k', label = '<(xn)2>')
legend(loc='upper left')
xlabel('time step')
grid()
ylabel('x2 average')
#savefig('x2average.pdf')
show()     

#plot r^2 average, we can see that the diffusion constant is approx. 1
figure()
plot(time, rsquare_ave,'k', label = '<r2>')
legend(loc='upper left')
xlabel('time step')
grid()
ylabel('r2 average')
#savefig('r2average.pdf')
show()  
        
