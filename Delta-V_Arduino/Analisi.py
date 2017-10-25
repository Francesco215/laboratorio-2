import numpy as np
import scipy as sp
import scipy.stats as stats
import scipy.optimize as optimize
import pylab as plt
from scipy.odr import odrpack

V, DV, X, DX =sp.loadtxt('dati.txt', unpack='true')

def Volt(x, a, b):
    return(a*x+b)
    
popt, pcov=optimize.curve_fit(Volt, X, V, sigma=DV, absolute_sigma='false' )
a, b=popt
Da, Db=np.sqrt(pcov.diagonal())
print('parametri di best-fit:')
print('a=%f+-%f' %(a, Da))
print('b=%f+-%f' %(b, Db))

def costant(a, x):
    return(a*x)

plt.figure(1)
plt.subplot(211)
plt.title('Calibrazione')
plt.xlabel('Digitale[digit]')
plt.ylabel('Voltaggio[V]')
plt.errorbar(X, V, DV, DX, '.')
plt.plot(np.linspace(0,1000, 10000), Volt(np.linspace(0,1000, 10000), a, b))

plt.subplot(212)
plt.plot((V-Volt(X, a, b))/DV, 'o')
plt.plot(costant(np.linspace(-100,-1200, 15), 0))
plt.xlim(-1,12)
plt.ylim(-1.5,2.5)
plt.show()

chi2=(((V-Volt(X, a, b))**2/(DV**2)).sum())/len(V)
print('Chi Quadro Normalizzato=%f' %chi2)

print(pcov)
corr=pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1])
print('corr(a;b)=%f' %corr)

#CALIBRAZIONE ALTERNATIVA
E=0.00477       #è il coeff. angolare della retta fittata con un unico parametro (vedi :"calibrazione alternativa")
DE=0.00029

def Volt_alt(x, a):
    return(a*x)

plt.figure(2)
plt.title('Calibrazione')
plt.xlabel('Digitale[digit]')
plt.ylabel('Voltaggio[V]')
plt.errorbar(X, V, DV, DX, '.')
plt.plot(np.linspace(0,1000, 10000), Volt(np.linspace(0,1000, 10000), a, b))
plt.plot(np.linspace(0,1000, 10000), Volt_alt(np.linspace(0,1000, 10000), E+DE))
plt.plot(np.linspace(0,1000, 10000), Volt_alt(np.linspace(0,1000, 10000), E-DE))
plt.show()
