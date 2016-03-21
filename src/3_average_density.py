# Read the output files by 3_gasmixing_v2.py
# Average the densities
# Plot the results

import numpy as np
import pylab as plt

W = 600  # width
m = 100  # average for the m step in the computation; can be set to 0~100
         # 0: first step; 100: last step
n = 100  # average over n trials

# initialize arrays
x = np.linspace(0,W,W+1)
rho_a = np.zeros(W+1)
rho_b = np.zeros(W+1)

# read and average the densities
for i in range(n):  # average the densities over n trials
    file = open(str(i)+'_rho_'+str(m)+'.dat','r')  # m: average for the m step in the computation 
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
#plt.title('Average linear density of gases',fontsize=22,fontweight='bold')
#plt.savefig('linear_density.pdf')
plt.show()
