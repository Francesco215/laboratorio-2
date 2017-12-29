#1 microfarad e
import numpy as np
import pylab

def RicercaMaxMin(y):
	massimi=np.array([])
	minimi=np.array([])
	for i in range(2,len(y)):
		if y[i-2]<=y[i-1] and y[i]<y[i-1] and y[i-1]>600: massimi=np.insert(massimi,len(massimi),int(i-1))
		if y[i-2]>=y[i-1] and y[i]>y[i-1] and y[i-1]<250: minimi=np.insert(minimi,len(minimi),int(i-1))
	return massimi.astype(int),minimi.astype(int)

risoluzione=50

def Triangolare(t,Ampiezza,T):
	funz=0
	for i in range(1,risoluzione,2):
		omega_i=2*np.pi*i/T
		c_i=4/(i*np.pi)**2
		funz=funz+c_i*np.cos(omega_i*t)
	return funz

def Quadra(t,Ampiezza,T):
	funz=0
	for i in range(1,risoluzione*5,2):
		omega_i=2*np.pi*i/T
		c_i=2/(i*np.pi)
		funz=funz+c_i*np.sin(omega_i*t)
	return funz

def Pinna(t,Ampiezza,T,omega_taglio):
	funz=0
	for i in range(1,risoluzione*2,2):
		omega_i=i*np.pi*2/T
		A_i=1/np.sqrt(1+(omega_i/omega_taglio)**2)
		c_i=2/(i*np.pi)
		phi_i=np.arctan(-omega_i/omega_taglio)
		funz=funz+Ampiezza*A_i*c_i*np.sin(omega_i*t+phi_i)
	return funz

def Attenuazione(frequenza,frequenza_taglio):
	return 1/np.sqrt(1+(frequenza/frequenza_taglio)**2)


pylab.xscale('log')
pylab.yscale('log')
pylab.plot(f,A)
pylab.show()



