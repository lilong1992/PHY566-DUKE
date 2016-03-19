import numpy as np
import pylab as plt

# parameters
L  = 100.0   # total length to solve
nx = 2000    # number of length steps
T  = 1.0     # total time to solve
nt = 10000   # number of time steps
D  = 2.0     # diffusion constant
H  = 50.0    # peak height at t = 0

dx = L/nx
dt = T/nt

# initialize u
u = np.zeros((nx+1,nt+1))
for i in range(int(nx/2-0.5/dx),int(nx/2+0.5/dx+1)):  # initial peak width = 1
    u[i,0] = H

# computational kernel: finite difference
k = D*dt/(dx**2)            # define a constant for convenience
for j in range(nt):         # time controled by j
    for i in range(1,nx):   # position controled by i
        u[i,j+1] = u[i,j] + k*(u[i+1,j]+u[i-1,j]-2*u[i,j])

# array for plotting
x = np.linspace(0,L,nx+1)

for i in range(6):
    print u[nx/2,i*nt/5]

# plot
plt.figure()
#plt.plot(x,u[:,0],'-r',label='t=0.0')
plt.plot(x,u[:,nt/5],'-r',label='t=0.2',linewidth=2)
plt.plot(x,u[:,2*nt/5],'-b',label='t=0.4',linewidth=2)
plt.plot(x,u[:,3*nt/5],'-y',label='t=0.6',linewidth=2)
plt.plot(x,u[:,4*nt/5],'-c',label='t=0.8',linewidth=2)
plt.plot(x,u[:,nt],'-m',label='t=1.0',linewidth=2)
plt.legend(fontsize=15,loc='upper right')
plt.xlabel('x',fontsize=20,fontweight='bold')
plt.ylabel('u',fontsize=20,fontweight='bold')
plt.xlim(40,60) # only plot the central part
plt.ylim(0,28)
plt.grid()
plt.xticks((40,50,60),(' ','0',' '),fontsize=14)
plt.yticks((0,12.5,25),('0','H/4','H/2'),fontsize=14)
#plt.title('1D diffusion equation',fontsize=22, fontweight='bold')
#plt.savefig('2b_1.pdf')
plt.show()

## Gaussian fit to find the variance
from scipy.optimize import curve_fit  #using curve_fit from scipy

def gauss(x, A, sigma):         #define a fitting function
    return A*np.exp(-(x-L/2)**2/(2.0*sigma**2))

time = np.linspace(0.2,1.0, 5)     # time at 0.2,0.4,0.6,0.8,1.0
sig = np.zeros(5)                  # to store sigma at different times
sig0 = np.sqrt(2.0*D*time)         #calculate sigma(t) = sqrt(2*D*t)

for i in range(5):             
    k = i+1
    y = u[:,k*nt/5]
    coeff, var_matrix = curve_fit(gauss,x,y) #fitting, returning an array:coeff[0] = A, coeff[1] =sigma
    sig[i] = abs(coeff[1]) #I don't know why when k=1 coeff[1] is negative on my computer
    print coeff

#plot sigma versus time
plt.figure()
plt.plot(time,sig,'k*',label='fitted $\sigma$(t)')
plt.plot(time,sig0,'rd',label='$\sigma$(t) from diffusion constant') #plot five points
plt.legend(fontsize=12,loc='upper left')
plt.xlabel('time',fontsize=20)
plt.ylabel('sigma',fontsize=20)
plt.xlim(0.1,1.1) 
#plt.ylim(0.0,2.5)
plt.grid()
#plt.title('1D diffusion equation_fit',fontsize=22, fontweight='bold')
#plt.savefig('group_2b_fit.pdf')
plt.show()
#the final result is that the fitted sigma is always a bit larger than the calculated one, but they 
#have the same trend...    
