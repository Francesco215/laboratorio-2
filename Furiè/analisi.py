
#1 microfarad e 6,94e8 ohm
import numpy as np 
import pylab
import os


freq_taglio=(1/(2*np.pi*1e-6*6.5e8))
freq_taglio2=105
risoluzione=100
def RicercaMaxMin(y,range_max,range_min):
	massimi=np.array([])
	minimi=np.array([])
	for i in range(2,len(y)):
		if y[i-2]<=y[i-1] and y[i]<y[i-1] and y[i-1]>range_max: massimi=np.insert(massimi,len(massimi),int(i-1))
		if y[i-2]>=y[i-1] and y[i]>y[i-1] and y[i-1]<range_min: minimi=np.insert(minimi,len(minimi),int(i-1))
	return massimi.astype(int),minimi.astype(int)

def Triangolare(t,Ampiezza,T,risoluzione):
	funz=0
	for i in range(1,risoluzione,2):
		omega_i=2*np.pi*i/T
		c_i=4/np.power(i*np.pi,2)
		funz=funz+c_i*np.cos(omega_i*t)
	return funz

def Quadra(t,Ampiezza,T,risoluzione):
	funz=0
	for i in range(1,risoluzione*5,2):
		omega_i=2*np.pi*i/T
		c_i=2/(i*np.pi)
		funz=funz+c_i*np.sin(omega_i*t)
	return funz

def Pinna(t,Ampiezza,T,omega_taglio,risoluzione):
	funz=0
	for i in range(1,risoluzione*2,2):
		omega_i=i*np.pi*2/T
		A_i=1/np.sqrt(1+np.power(omega_i/omega_taglio,2))
		c_i=2/(i*np.pi)
		phi_i=np.arctan(-omega_i/omega_taglio)
		funz=funz+Ampiezza*A_i*c_i*np.sin(omega_i*t+phi_i)
	return funz

def QuadraBrutta(t,Ampiezza,T,tau,risoluzione):
	if tau>T: return 0
	delta=T/tau
	funz=tau/T
	for i in range(2,risoluzione*5,2):
		a_i=2/(i*np.pi)
		b_i=i*np.pi*tau/T
		c_i=i/T
		funz=funz+Ampiezza*a_i*np.sin(b_i)*np.cos(c_i*t)
	return funz

def Sega(t,Ampiezza,T,tau,omega_taglio,risoluzione):
	delta=T/tau
	funz=tau/T
	for i in range(2,risoluzione*5,2):
		omega_i=i*np.pi*2/T
		a_i=2/(i*np.pi)
		b_i=i*np.pi*tau/T
		c_i=i/T
		A_i=1/np.sqrt(1+np.power(omega_i/omega_taglio,2))
		phi_i=np.arctan(-omega_i/omega_taglio)
		funz=funz+Ampiezza*A_i*a_i*np.sin(b_i)*np.cos(c_i*t+phi_i)
	return funz


def Attenuazione(frequenza,frequenza_taglio,a):
	return a/np.sqrt(1+(frequenza/frequenza_taglio)**2)
 
#esercizio 1
x=np.linspace(0,10,1000)
for i in range(1,12):
	y=Triangolare(x,1,1,2**i)
	pylab.plot(x,y)
	pylab.xlabel('tempo[s]')
	pylab.ylabel('Volt[V]')
	pylab.title('triangolare con '+str(2**i)+' iterazioni')
	pylab.savefig('esercizio_1/triangolare/'+str(2**(i))+'.png')
	pylab.close()
	y=Quadra(x,1,1,2**i)
	pylab.xlabel('tempo[s]')
	pylab.ylabel('Volt[V]')
	pylab.title('quadra con '+str(2**i)+' iterazioni')
	pylab.plot(x,y)
	pylab.savefig('esercizio_1/quadra/'+str(2**(i))+'.png')
	pylab.close()
	y=QuadraBrutta(x,1,1,1/3,2**i)
	pylab.xlabel('tempo[s]')
	pylab.ylabel('Volt[V]')
	pylab.title('quadra con '+str(2**i)+' iterazioni')
	pylab.plot(x,y)
	pylab.savefig('esercizio_1/quadra_brutta/'+str(2**(i))+'.png')
	pylab.close()

n=4
#esercizio 2
for i in range(0,12):
	T_i=2**(-i)
	x=np.linspace(0,2**(-i+2),1000)
	y=Pinna(x,1,T_i,3e2,risoluzione)
	pylab.plot(x,y)
	pylab.xlabel('tempo[s]')
	pylab.ylabel('Volt[V]')
	pylab.savefig('esercizio_2/pinna/'+str(2**(i))+'hz.png')
	pylab.close()
	y=Sega(x,1,T_i,T_i/n,3e2,risoluzione)
	pylab.plot(x,y)
	y=QuadraBrutta(x,1,T_i,T_i/n,risoluzione)
	pylab.plot(x,y)
	y=np.zeros(1000)+1/n
	pylab.plot(x,y)
	pylab.xlabel('tempo[s]')
	pylab.ylabel('Volt[V]')
	pylab.savefig('esercizio_2/sega/'+str(2**(i))+'hz.png')
	pylab.close()
#esercizio 2 bis
t,V=np.loadtxt('dati/35hz.txt',unpack='true')
massimi,minimi=RicercaMaxMin(V,max(V)-100,min(V)+100)
x=np.linspace(0,t[-1],len(t)*10)
y=Pinna(x,V[massimi[1]]-V[minimi[1]],t[massimi[1]]-t[massimi[2]],freq_taglio,risoluzione)

V=V-(V[massimi[1]]+V[minimi[1]])/2
pylab.plot(x,y)
pylab.plot(t,V)
pylab.savefig('esercizio_2/bis/35hz.png')
#pylab.show()
pylab.close()

#esercizio 3
file=np.loadtxt('dati/Filtro_rc_ampiezza.txt')
Vout,dVout,f,df=np.transpose(file)
pylab.errorbar(f,Vout,dVout,df,'.')
x=np.linspace(np.log(f[0]),np.log(f[-1]),100)
x=np.power(np.e,x)
y=Attenuazione(x,freq_taglio2,5.96)
pylab.xscale('log')
pylab.yscale('log')
pylab.plot(x,y)
pylab.xlabel('frequenza [hz]')
pylab.ylabel('Vout [V]')
pylab.savefig('esercizio_3/filtro_RC.png')
#pylab.show()
pylab.close()
