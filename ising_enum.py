import os
import numpy as np
import matplotlib.pyplot as plt
import sys    

L=4
Nsite = L*L
Nstate=int(pow(2,Nsite))
latt='sqlatt_PBC'
def get_mag(spin):    
    return np.sum(spin)

def get_ener(spin):    
    sp = np.reshape(spin, (L,L))
    spx = np.roll(sp,1,axis=1)
    spy = np.roll(sp,1,axis=0)  
    return -(np.dot(spin,spx.flatten()) + np.dot(spin,spy.flatten()))

#E_t = []
#C_t = []
#X_t = []
#if(os.path.isfile('Nlin%f_latt%s_enum.out' %(L,latt))):
#	os.remove('Nlin%f_latt%s_enum.out' %(L,latt))

for T in np.arange(2.0,2.1,.1):
	e = 0
	e_2 = 0
	m_2 = 0
	Z = 0
	m_4 = 0
	beta = 2 
	T = 1/beta
	for state in range(Nstate):

	   svec=np.array(list(np.binary_repr(state).zfill(Nsite))).astype(np.int8)
	   spin=2*svec-1
	   mag=get_mag(spin)
	   ener=get_ener(spin)

	   print ('STATE = ',state)
	   print (np.reshape(spin,(L,L)))
	   print ('M = ',mag,'; E = ',ener)
	   print ()

	   e += (ener/Nsite) * np.exp(-ener/T)
	   e_2 += ((ener/Nsite)**2) * np.exp(-ener/T)
	   m_2 += ((mag/Nsite)**2) * np.exp(-ener/T)
	   Z += np.exp(-ener/T)
	   m_4 += ((mag/Nsite)**4) * np.exp(-ener/T)

	e = e/Z
	e_2 = e_2/Z
	m_2 = m_2/Z
	m_4 = m_4/Z
	Cv=(Nsite/T**2)*(e_2-e**2)
	X =(Nsite/T)*(m_2)
	Ul=(3/2)*(1 - m_4 / (3*(m_2**2)))
#	outfile = open('Nlin%f_latt%s_enum2.out' %(L,latt), 'a')
#	outfile.write('%f %f %f\n' %(T, Cv, X))
	#E_t.append(e)
	#C_t.append((Nsite/T**2)*(e_2-e**2))
	#X_t.append((Nsite/T)*(m_2))
print("energy = ", e)
print("energy sq = ", e_2)
print("mag sq = ", m_2)
print("Susceptability = ", X)
print("Heat Capacity = ", Cv)
print("Binder Parameter = ", Ul)
#T = np.arange(1,50,.1)
#plt.plot(T, E_t)
#plt.xlabel('T')
#plt.ylabel('e')
#plt.title('e vs T')
#plt.grid(True)
#plt.show()

#plt.plot(T,C_t)
#plt.ylabel('$C_v$')
#plt.title('$C_v$ vs T')
#plt.grid(True)
#plt.show()

#plt.plot(T,X_t)
#plt.ylabel('$X_v$')
#plt.title('$X_v$ vs T')
#plt.grid(True)
#plt.show()


