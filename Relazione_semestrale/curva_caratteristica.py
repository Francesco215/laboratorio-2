import numpy as np
import pylab
from scipy.optimize import curve_fit

dati=['dati/prima_parte/V1_e_V2.txt']

Volt=np.loadtxt(dati[0], unpack='true')
calibrazione=[0.00477,0.00029]
Volt=np.array([Volt*calibrazione[0],Volt*calibrazione[1]])
R=([680,33])
I=[(Volt[0]-Volt[1])/R[0],2*calibrazione[0]/R[0]+(Volt[0]-Volt[1])*R[1]/(R[0]**2)]

def esponenziale(x, a, b,c):
	return a*(np.exp(x/b)-1)+c

def dEsponenziale(x,a,b,c):
	return esponenziale(x,a,b,c)/b

risoluzione=500 
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

coso=20
p_0=[0,(Volt[1][-1]-Volt[1][coso])/np.log(I[0][-1]/I[0][coso]),0]
popt,pcov=curve_fit(esponenziale, Volt[1],I[0],p_0,absolute_sigma='false')
for i in range(0,10):
	I[1]=np.sqrt(I[1]**2+(V[1]*dEsponenziale(V[0],*popt))**2)
	popt,pcov=curve_fit(esponenziale,Volt[1],I[0],popt,sigma=I[i],absolute_sigma='false')

chi2=(((I[0]-esponenziale(Volt[1],*popt))/I[1])**2).sum()

print("chi2 normalizzato=",chi2/len(I[0]))
print("parametri ottimali: A=",popt[0]," tau=",popt[1]," intercetta=",popt[2])
print("covarianza tra a e b (guarda funzione esponenziale)",pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1]))
print("errori associati ai parametri ottimali",pcov.diagonal())

pylab.figure(1)
pylab.subplot(211)
pylab.errorbar(Volt[1],I[0],I[1],calibrazione[0],'.')
x=np.linspace(0,145*calibrazione[0],500)
y=esponenziale(x,*popt)
pylab.plot(x,y)
pylab.xlabel('Delta V[V]')
pylab.ylabel('Intensità[A]')
pylab.subplot(212)
pylab.plot(Volt[1],(I[0]-esponenziale(Volt[1],*popt))/I[1],'.')
pylab.xlabel('Delta V[V]')
pylab.ylabel('Residui intensità[A]')
y=np.zeros(len(x))
pylab.plot(x,y)
pylab.savefig('fit.png')
pylab.close()

fig=pylab.figure()
tau=5*2
a=4	#indica il numero di quadratini nell'immagine
T_i=1	#indica quantè lungo il periodo dell'oscillazione
for i in range(0,2*a):
	taglio_i=3e2*2**(-i)
	ax=fig.add_subplot(a,2,i+1)
	x=np.linspace(0,4*T_i,1000)
	y=Sega(x,1,T_i,T_i/tau,taglio_i)
	ax.plot(x,y)
	y=QuadraBrutta(x,1,T_i,T_i/tau)
	ax.plot(x,y)
	y=np.zeros(1000)+1/tau
	ax.plot(x,y)
	ax.set_title('freq. taglio='+str(taglio_i))
fig.subplots_adjust(hspace=1)
pylab.savefig('integratore.png')
