import numpy as np
import pylab
from scipy.optimize import curve_fit
from scipy import stats

Volt=np.loadtxt('dati/DATI_GABRIELE.txt', unpack='true')
calibrazione=[0.00477,0.00029]
Volt=Volt*calibrazione[0]
R=([680,33])
I=[(Volt[0]-Volt[1])/R[0],2*calibrazione[0]/R[0]+(Volt[0]-Volt[1])*R[1]/(R[0]**2)]


def esponenziale(x, a, b,c):
	return a*(np.exp(x/b)-1)+c
def costant(x, a):
	return(a*x)


coso=20
p_0=[0,(Volt[1][-1]-Volt[1][coso])/np.log(I[0][-1]/I[0][coso]),0]
popt,pcov=curve_fit(esponenziale, Volt[1],I[0],p_0,absolute_sigma='false')
chi2=(((I[0]-esponenziale(Volt[1],*popt))/I[1])**2).sum()

print("chi2 normalizzato=",chi2/len(I[0]))
print("covarianza tra a e b (guarda funzione esponenziale)"pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1]))
print("errori associati ai parametri ottimali"pcov.diagonal())

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
y=costant(x,0)
pylab.plot(x,y,)
pylab.show()
