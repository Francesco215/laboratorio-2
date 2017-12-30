
#1 microfarad e 6,94e8 ohm
import numpy as np
import pylab
import os

freq_taglio=(1/(2*np.pi*1e-6*6.94e8))
risoluzione=100
def RicercaMaxMin(y,range_max,range_min):
	massimi=np.array([])
	minimi=np.array([])
	for i in range(2,len(y)):
		if y[i-2]<=y[i-1] and y[i]<y[i-1] and y[i-1]>range_max: massimi=np.insert(massimi,len(massimi),int(i-1))
		if y[i-2]>=y[i-1] and y[i]>y[i-1] and y[i-1]<range_min: minimi=np.insert(minimi,len(minimi),int(i-1))
	return massimi.astype(int),minimi.astype(int)

def Triangolare(t,Ampiezza,T):
	funz=0
	for i in range(1,risoluzione,2):
		omega_i=2*np.pi*i/T
		c_i=4/np.power(i*np.pi,2)
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
		A_i=1/np.sqrt(1+np.power(omega_i/omega_taglio,2))
		c_i=2/(i*np.pi)
		phi_i=np.arctan(-omega_i/omega_taglio)
		funz=funz+Ampiezza*A_i*c_i*np.sin(omega_i*t+phi_i)
	return funz

def Attenuazione(frequenza,frequenza_taglio):
	return 1/np.sqrt(1+(frequenza/frequenza_taglio)**2)

file=np.loadtxt('Filtro_rc_ampiezza.txt')
Vout,dVout,f,df=np.transpose(file)
pylab.errorbar(f,Vout,dVout,df,'.')
x=np.linspace(np.log(f[0]),np.log(f[-1]),100)
x=np.power(np.e,x)
y=Attenuazione(x,freq_taglio)
pylab.plot(x,y)
pylab.xscale('log')
pylab.yscale('log')
pylab.show()

"""
t,V=np.loadtxt('dati/25hz.txt',unpack='true')

massimi,minimi=RicercaMaxMin(V,max(V)-100,min(V)+100)
x=np.linspace(0,t[-1],len(t))
y=Pinna(x,V[massimi[1]]-V[minimi[1]],t[massimi[1]]-t[massimi[2]],freq_taglio)

V=V-(V[massimi[1]]+V[minimi[1]])/2
pylab.plot(x,y)
pylab.plot(t,V)
pylab.savefig('immagini/25hz.png')
pylab.show()
"""


