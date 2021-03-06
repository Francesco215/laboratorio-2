import numpy as np
import scipy as sp
import scipy.optimize as optimize
from scipy.odr import odrpack
import scipy.stats as stats
import pylab as plt

#PROCESSO DI CARICA
t, V=np.loadtxt('asd_C3.txt', unpack='true')
Dt, DV=4, 1         #Valori nominali dati dalla risoluzione strumentale

def Volt(x, a, b):
    return(a*(1-np.exp(-t/b)))
    
popt, pcov=optimize.curve_fit(Volt, t, V, (1000, 23), sigma=DV, absolute_sigma='false')
Vz, tau=popt
DVz, Dtau=np.sqrt(pcov.diagonal())
print('V_0_carica=%f+-%f'%(Vz, DVz))
print('tau_carica=%f+-%f' %(tau, Dtau))
ndof=len(V)-2       #gradi di libertà
chi2_norm_carica=((V-Volt(t, Vz, tau)/DV)**2).sum()/ndof
print('Chi Quadro_norm_carica=%f' %(chi2_norm_carica))
corr=pcov[0][1]/np.sqrt(pcov[0][1]*pcov[1][0])
print('Corr(V_0, tau)_carica=%f' %corr)
def costant(x, a):          #serve solo per tracciare linea dritta nel grafico degli scarti
    return(a*x)

plt.figure(1)
plt.subplot(211)
plt.title('CAPACITOR CHARGE')
plt.xlabel('Tempo [us]')
plt.ylabel('DV [digit]')
plt.errorbar(t, V, Dt, DV, '.')
x=np.linspace(0,30000,1000)
y=np.array([])
for i in range (0,len(x)):
	y=np.insert(y,len(y),x[i])
print(len(x),len(y))
plt.plot(x,y)
plt.subplot(212)
plt.plot(np.linspace(0, 260, 1000), costant(np.linspace(0, 260, 1000), 0))
plt.plot((V-Volt(t, Vz, tau))/DV, 'o')
plt.show()
print('-------------')

#♠PROCESSO DI SCARICA
t, V=np.loadtxt('asd_S3.txt', unpack='true')
Dt, DV=4, 1

def Volt(x, a, b, c):
    return(a*np.exp(-t/b)+c)
    
popt, pcov=optimize.curve_fit(Volt, t, V, (1000, 23, 0), sigma=DV, absolute_sigma='false')
Vz, tau, c=popt
DVz, Dtau, Dc=np.sqrt(pcov.diagonal())
print('V_0_scarica=%f+-%f'%(Vz, DVz))
print('tau_scarica=%f+-%f' %(tau, Dtau))
print('Costante di Offset=%f+-%f' %(c, Dc))
chi2_norm_scarica=((V-Volt(t, Vz, tau, c)/DV)**2).sum()/ndof
print('Chi QUadro_norm_scarica=%f' %(chi2_norm_scarica))
corr=pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1])
print('Corr(VZ_0, tau)_scarica=%f' %corr)

def costant(x, a):
    return(a*x)

plt.figure(2)
plt.subplot(211)
plt.title('CAPACITOR DISCHARGE')
plt.xlabel('Tempo [us]')
plt.ylabel('DV [digit]')
plt.errorbar(t, V, Dt, DV, '.')
plt.plot(t, Volt(t, Vz, tau, c))
plt.subplot(212)
plt.plot(np.linspace(0, 260, 1000), costant(np.linspace(0, 260, 1000), 0))
plt.plot((V-Volt(t, Vz, tau, c))/DV, 'o')
plt.show()
