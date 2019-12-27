import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def func(x, mag_ext, A, B, C):
	return mag_ext + A*x + B*x**2 + C*x**3

beta=0.75
for i in range(2, 13, 1):
	#load text
	beta = round(beta,2)
	data = np.loadtxt("/Users/Alex/Documents/SPS/python_programs/symmbreak_beta"+str(beta)+".out")
	x = data[:,0]
	y = data[:,1]
	dy = data[:,2]
	
	#Non-linear fitting 
	xfit = np.linspace(min(x), max(x), 100)
	popt, pcov = curve_fit(func, x, y, sigma=dy)
	#plt.plot(xfit, func(xfit, *popt))
	#plt.errorbar(x, y, yerr=dy, linestyle='None', marker='o', color='black')
	print('mag_extrap = ', popt[0])
	temp = 1/beta
	plt.plot(temp, popt[0], linestyle='None', marker='o', color='blue')
	beta+=0.05

plt.ylabel(r'$\langle m^2 \rangle_{ex}$')
plt.xlabel('Temperature')
plt.title(r'$\langle m^2 \rangle$ for Different Temperatures')
plt.show()
