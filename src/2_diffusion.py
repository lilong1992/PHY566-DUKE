import numpy as np
import pylab as plt

# parameters
L  = 100.0   # total length to solve
nx = 1000    # number of length steps
T  = 1.0     # total time to solve
nt = 10000   # number of time steps
D  = 2.0     # diffusion constant
H  = 50.0    # peak height at t = 0

dx = L/nx
dt = T/nt

# initialize u
u = np.zeros((nx+1,nt+1))
for i in range(int(nx/2-1/dx),int(nx/2+1/dx+1)):  # initial peak width = 2
    u[i,0] = H

# computational kernel: finite difference
k = D*dt/(dx**2)            # define a constant for convenience
for j in range(nt):         # time controled by j
    for i in range(1,nx):   # position controled by i
        u[i,j+1] = u[i,j] + k*(u[i+1,j]+u[i-1,j]-2*u[i,j])

# array for plotting
x = np.linspace(0,L,nx+1)

# plot
plt.figure()
plt.plot(x,u[:,0],'-r',label='t=0.0')
plt.plot(x,u[:,nt/5],'-b',label='t=0.2')
plt.plot(x,u[:,2*nt/5],'-y',label='t=0.4')
plt.plot(x,u[:,3*nt/5],'-g',label='t=0.6')
plt.plot(x,u[:,4*nt/5],'-c',label='t=0.8')
plt.plot(x,u[:,nt],'-m',label='t=1.0')
plt.legend(fontsize=12,loc='upper right')
plt.xlabel('x',fontsize=20,fontweight='bold')
plt.ylabel('u',fontsize=20,fontweight='bold')
plt.xlim(40,60) # only plot the central part
plt.ylim(0,60)
plt.grid()
plt.xticks((40,50,60),(' ','L/2',' '),fontsize=12)
plt.yticks((0,12.5,25,37.5,50),('0',' ','H/2',' ','H'),fontsize=12)
#plt.title('1D diffusion equation',fontsize=22, fontweight='bold')
#plt.savefig('group_2b.pdf')
plt.show()