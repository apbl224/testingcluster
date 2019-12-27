import os
import random
import numpy as np
import matplotlib.pyplot as plt

Neql=1000.0;
Nmcs=1000.0; Nbin=100.0; SEED=random.randint(0,1000);
latt="sqlatt_PBC";

beta=0.75
outfile=open('symmbreak_beta'+str(beta)+'.out', 'w')

for L in np.arange(5,100,5):
	pfile=open('param.dat', 'w')
	pfile.write('%d %f %d %d\n' %(L,beta,Neql,Nmcs))
	pfile.write('%d %d %s\n'%(Nbin,SEED,latt))
	pfile.close()
	os.system('./a.out >> spin.log')

	data=np.loadtxt('data.out')
	m_2 = data[:,3]

	# print to data file
	outfile.write('%f %f %f\n' %(1/L, np.average(m_2), np.std(m_2)/np.sqrt(Nbin-1)))
	#plot the data 
	print("Nlin= ", L) #show progress of program
	plt.errorbar(1/L, np.average(m_2),yerr=np.std(m_2)/np.sqrt(Nbin-1), linestyle='None',color='green', marker='o')

plt.xlabel("Lattice Size (1/L)") 
plt.ylabel(r'$\langle m^2 \rangle$')
plt.title("Average $m^2$ vs. Inverse Lattice Size for "+r'$\beta$='+str(beta))
plt.show()
