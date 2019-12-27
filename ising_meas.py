import os
import random
import numpy as np
import matplotlib.pyplot as plt

Nlin=3.0; Neql=1000.0;
Nmcs=10000.0; Nbin=1000.0; SEED=random.randint(0,1000);
latt="sqlatt_PBC";

if(os.path.isfile('Nlin%d_latt%s_wolff.out' %(Nlin,latt))):
        os.remove('Nlin%d_latt%s_wolff.out' %(Nlin,latt))


for T in np.arange(1.,1.1,.1):
	beta=1
	pfile=open('param.dat', 'w')
	pfile.write('%d %f %d %d\n' %(Nlin,beta,Neql,Nmcs))
	pfile.write('%d %d %s\n'%(Nbin,SEED,latt))
	pfile.close()
	os.system('./a.out >> spin.log')

	data=np.loadtxt('data.out')
	e = data[:,0]
	e_2 = data[:,1]
	m = data[:,2]
	m_2 = data[:,3]
	m_4 = data[:,4]
	
	Nsite=Nlin**2
	Cv = (Nsite*(beta**2))*(np.average(e_2) -(np.average(e)**2))
	X = (Nsite*beta)*(np.average(m_2))
	Ul = (3/2)*(1 - (np.average(m_4)/(3*np.average(m_2)**2)))
	outfile=open('Nlin%d_latt%s_wolff.out' %(Nlin,latt), 'a')
	outfile.write('%f %f %f %f %f\n' %(T, Cv, X, (m_2.std()/np.sqrt(Nbin-1)), Ul))
print("<e> = ",np.average(e))
print("error = ", e.std()/np.sqrt(Nbin-1))
print("<e2> = ",np.average(e_2))
print("<m> = ",np.average(m))
print("<m2> = ",np.average(m_2))

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

print("Specific Heat = ",Cv)
print("error = ", np.sqrt(np.sum(Cv_bs**2)/float(Nbs) - (np.sum(Cv_bs)/float(Nbs))**2))
print("Susceptability = ",X)
print("error = ", m_2.std()/np.sqrt(Nbin-1))
print("Binder parameter = ", Ul)
print("error = ", np.sqrt(np.sum(Ul_bs**2)/float(Nbs) - (np.sum(Ul_bs)/float(Nbs))**2))  

