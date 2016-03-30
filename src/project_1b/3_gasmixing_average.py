import numpy as np
import random as rd
import pylab as plt

def move_random(steps):  # pick one particle and move steps steps
    global u,available
    # pick one site from the available list
    pick = rd.randint(0,160000-1)
    i = available[pick][0]
    j = available[pick][1]
    dice = rd.random()
    if dice < 0.25:
        if j-steps >= 0 and u[i,j-steps] == 0: #left
            u[i,j-steps] = u[i,j]
            u[i,j] = 0
            available[pick] = [i,j-steps]  # renew the position
    elif dice < 0.5:
        if j+steps < W and u[i,j+steps] == 0:  # right
            u[i,j+steps] = u[i,j]
            u[i,j] = 0
            available[pick] = [i,j+steps]
    elif dice < 0.75:
        if i-steps >= 0 and u[i-steps,j] == 0:  # down
            u[i-steps,j] = u[i,j]
            u[i,j] = 0
            available[pick] = [i-steps,j]
    else:
        if i+steps < H and u[i+steps,j] == 0:  # up
            u[i+steps,j] = u[i,j]
            u[i,j] = 0
            available[pick] = [i+steps,j]

def density(u):  # evaluate linear population densities
    r_a = np.zeros(W)
    r_b = np.zeros(W)
    for j in range(W):
        for i in range(H):
            if u[i,j] == -1:
                r_a[j] += 1
            elif u[i,j] == 1:
                r_b[j] += 1
    return r_a,r_b

# initialize u
H = 400  # height of area
W = 600  # width of area, should be a multiple of 3
u = np.zeros((H,W))
available = np.zeros((160000,2))  # store positions of all particles
for i in range(H):
    for j in range(W/3):
        u[i,j] = -1
        available[i*W/3+j] = [i,j]
    for j in range(2*W/3,W):
        u[i,j] = 1
        available[i*W/3+j+79600] = [i,j]

# linear population densities
rho_a = np.zeros(W)
rho_b = np.zeros(W)
x = np.linspace(0,W-1,W)  # used for plotting

# average the final configuration over 100 trials
for average in range(100):
    print average
    # mixing gases
    for m in range(2001):
        for n in range(10000):
            move_random(200)
    temp1,temp2 = density(u)  # linear population densities
    # sometimes code crashes before 100 runs are finished
    # write to files for post-processing
    output = open('rho_'+str(average)+'.dat','w')  # output
    for i in range(W):
        output.write('%10.6f  %10.6f  %10.6f\n' % (x[i],temp1[i],temp2[i]))
    output.close()
    rho_a += temp1/100.0
    rho_b += temp2/100.0

plt.figure()
plt.plot(x,rho_a,'-r',label='particle A',linewidth=2)
plt.plot(x,rho_b,'-b',label='particle B',linewidth=2)
plt.legend(loc='upper center')
plt.xlabel('x',fontsize=20,fontweight='bold')
plt.ylabel('density',fontsize=20,fontweight='bold')
plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
plt.ylim(0,450)
plt.yticks((0,200,400),('0','200','400'),fontsize=14)
#plt.title('Mixing two gases',fontsize=22,fontweight='bold')
plt.savefig('density_average.pdf')
plt.show()