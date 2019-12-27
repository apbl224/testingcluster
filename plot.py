#Plot the specific heat and binder parameter for different lattice sizes

import os
import random
import numpy as np
import matplotlib.pyplot as plt
 
Neql=1000.0;
Nmcs=1000.0; Nbin=100.0; SEED=random.randint(0,1000);
latt="sqlatt_PBC";

for L in range(20,60,10):
	outfile=open('data'+str(L)+'zoom.out', 'w')
	for beta in np.arange(0.40, 0.45, 0.001):
		pfile=open('param.dat', 'w')
		pfile.write('%d %f %d %d\n' %(L,beta,Neql,Nmcs))
		pfile.write('%d %d %s\n'%(Nbin,SEED,latt))
		pfile.close()
		os.system('./a.out >> spin.log')
		
		print('Lattice Size = ', L)
		print('Beta = ', round(beta, 3))

		data=np.loadtxt('data.out')
		e = data[:,0]
		e_2 = data[:,1]
		m_2 = data[:,3]
		m_4 = data[:,4]
  
		Nsite=L**2
		Cv = (Nsite*(beta**2))*(np.average(e_2) -(np.average(e)**2))
		Ul = (3/2)*(1 - (np.average(m_4)/(3*np.average(m_2)**2)))
		
		#Calculate error in Cv and Ul using the bootstrap method
		Nbs=50
		samplesize=len(e)
		Cv_bs = np.zeros(Nbs)
		Ul_bs = np.zeros(Nbs)
		for step in range(Nbs):
			e_new = np.zeros(samplesize)
			e_2_new = np.zeros(samplesize)
			m_2_new = np.zeros(samplesize)
			m_4_new = np.zeros(samplesize)
			for sample in range(samplesize):
				ind = random.randint(0,samplesize-1)
				e_new[sample] = e[ind]
				e_2_new[sample] = e_2[ind]
				m_2_new[sample] = m_2[ind]
				m_4_new[sample] = m_4[ind]
			Cv_bs[step] = (Nsite*(beta**2))*(np.average(e_2_new) -(np.average(e_new)**2))
			Ul_bs[step] = (3/2)*(1 - (np.average(m_4_new)/(3*np.average(m_2_new)**2)))

			error_Cv = np.sqrt(np.sum(Cv_bs**2)/float(Nbs) - (np.sum(Cv_bs)/float(Nbs))**2) 
			error_Ul = np.sqrt(np.sum(Ul_bs**2)/float(Nbs) - (np.sum(Ul_bs)/float(Nbs))**2)  
		 
		T = 1/beta
		outfile.write('%f %f %f %f %f\n' %(T, Cv, error_Cv, Ul, error_Ul))
	outfile.close()
	data1 = np.loadtxt(outfile.name)
	plt.figure(1)
	plt.errorbar(data1[:,0], data1[:,1], yerr=data1[:,2], label='L='+str(L))
	plt.figure(2)
	plt.errorbar(data1[:,0], data1[:,3], yerr=data1[:,4], label='L='+str(L))
plt.figure(1)
plt.xlabel('Temperature')
plt.ylabel(r'$C_v$')
plt.title('Specific Heat')
plt.legend()
plt.figure(2)
plt.xlabel('Temperature')
plt.ylabel(r'$U_l$')
plt.title('Binder Parameter')
plt.legend()
plt.show()


