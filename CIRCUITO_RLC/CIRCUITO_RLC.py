import numpy as np
import scipy.optimize as optimize
import pylab as plt
import scipy.stats as stats
from uncertainties import ufloat

#DATI
t, Dt , V, DV=np.loadtxt('/Users/francescopaolo/Desktop/UNIVERSITY/LABORATORIO/LABORATORIO_2/ESPERIENZE/CIRCUITO_RLC/DATAS/ave_ramen.txt', unpack='true')
#DV, Dt=(1., 1.74)

def Volt(x, A, tau, w, phi, Vbias):
	return(A*np.exp(-x/tau)*np.cos(w*x+phi)+Vbias)

'''
parameters=optimize.differential_evolution(Volt, [[300, 1300], [0, 100], [0, 10], [-3.14, 3.14], [300, 500]])
print(parameters)
print(type(parameters))
'''

popt, pcov=optimize.curve_fit(Volt, t, V, (300, 1900, 5e-3, 2.5, 480), DV) #, absolute_sigma='true')

A, tau, w, phi, Vbias=popt
DA, Dtau, Dw, Dphi, DVbias=np.sqrt(pcov.diagonal())
chi2=(((Volt(t, A, tau, w, phi, Vbias)-V)**2)/(Dt**2)).sum()/len(V)

print('A=%f+-%f' %(A, DA))
print('tau=%f+-%f' %(tau, Dtau))
print('w=%f+-%f' %(w, Dw))
print('phi=%f+-%f' %(phi, Dphi))
print('Vbias=%f+-%f' %(Vbias, DVbias))
print('tau=%f+-%f' %(tau, Dtau))
print('chi2=%f' %chi2)

def costant(x, a):
	return(a*x)

plt.figure(1)
plt.subplot(211)
plt.title(r'$RLC(C=1uF)$')
plt.xlabel('Tempo[us]')
plt.ylabel('Voltaggio[digit]')
plt.errorbar(t, V, DV, Dt, '.')
plt.plot(np.linspace(0, 14000, 4000), Volt(np.linspace(0, 14000, 4000), A, tau, w, phi, Vbias))
plt.subplot(212)
plt.plot(V-Volt(t, A, tau, w, phi, Vbias), 'o')
plt.plot(np.linspace(0, 250, 10), costant(np.linspace(0, 250, 10), 0))
plt.show()

W=ufloat(w, Dw)
Tau=ufloat(tau, Dtau)
C=ufloat(0.1*np.exp(-6), 0.01*np.exp(-6))
T=2*np.pi/W
print('Periodo(t)=') 
print(T) 
R=T**2/(2*np.pi**2*C*Tau)
print('Resistenza stimata=')
print(R)
L=T**2/(2*np.pi**2+C*Tau)
print('Induttanza=')
print(L)
Qf=W*Tau/2
print('Fattore di Qual.')
print(Qf)