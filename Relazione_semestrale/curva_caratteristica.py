import numpy as np
import pylab
from scipy.optimize import curve_fit

#acquisizione dati e 
dati=['dati/prima_parte/V1_e_V2.txt']
Volt=np.loadtxt(dati[0], unpack='true')
calibrazione=[0.00477,0.00029]
Volt=np.array([Volt*calibrazione[0],Volt*calibrazione[1]])
R=([680,33])
I=[(Volt[0]-Volt[1])/R[0],2*calibrazione[0]/R[0]+(Volt[0]-Volt[1])*R[1]/(R[0]**2)]

#funzioni
def esponenziale(x, a, b,c):
	return a*(np.exp(x/b)-1)+c

def dEsponenziale(x,a,b,c):
	return (a/b)*np.exp(x/b)

#fit (non funzionante)
coso=20
p_0=[0,(Volt[1][-1]-Volt[1][coso])/np.log(I[0][-1]/I[0][coso]),0]
popt,pcov=curve_fit(esponenziale, Volt[1],I[0],p_0,absolute_sigma='false')
for i in range(0,10):
	I[1]=np.sqrt(I[1]**2+(V[1]*dEsponenziale(V[0],*popt))**2)
	popt,pcov=curve_fit(esponenziale,Volt[1],I[0],popt,sigma=I[i],absolute_sigma='false')

chi2=(((I[0]-esponenziale(Volt[1],*popt))/I[1])**2).sum()

#stampa i parametri di fit
print("chi2 normalizzato=",chi2/len(I[0]))
print("parametri ottimali: A=",popt[0]," tau=",popt[1]," intercetta=",popt[2])
print("covarianza tra a e b (guarda funzione esponenziale)",pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1]))
print("errori associati ai parametri ottimali",pcov.diagonal())

#figura
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
