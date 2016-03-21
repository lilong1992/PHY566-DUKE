import numpy as np
import pylab as plt

W = 600  # width
n = 100  # average over n trials

# initialize arrays
x = np.linspace(0,W-1,W)
rho_a = np.zeros(W)
rho_b = np.zeros(W)

# read and average the densities
for i in range(n):  # average over n trials
    file = open('rho_'+str(i)+'.dat','r') 
    j = 0
    for line in file:
        columns = line.split()
        rho_a[j] += float(columns[1])/n
        rho_b[j] += float(columns[2])/n
        j += 1
    file.close

# plot
plt.figure()
plt.plot(x,rho_a,'-r',label='particle A',linewidth=2)
plt.plot(x,rho_b,'-b',label='particle B',linewidth=2)
plt.legend(loc='upper center')
plt.xlabel('x',fontsize=20,fontweight='bold')
plt.ylabel('density',fontsize=20,fontweight='bold')
plt.xticks((0,200,400,600),('0','200','400','600'),fontsize=14)
plt.ylim(0,450)
plt.yticks((0,200,400),('0','200','400'),fontsize=14)
#plt.title('Average linear population density of two gases',fontsize=22,fontweight='bold')
#plt.savefig('linear_population_density'.pdf')
plt.show()