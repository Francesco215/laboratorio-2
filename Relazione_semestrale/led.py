import numpy as np
import pylab
from scipy.optimize import curve_fit

def curva_caratteristica(I,V,etaV):
	return I*(np.exp(V/etaV)-1)
#calcola la differenza di potenziale del fotodiodo in funzione di quella del led
def funzione(V_0,I_0,etaV,k,a,R_I,c):
	I=curva_caratteristica(I_0,V_0,etaV)
	gamma=a*I+1
	F=1+(R_I*gamma*I*V_0) #Rb_I è il rapporto tra R*b/I_0
	return -k*np.log(np.abs(F))+c #k è ubuale a eta_1*V_T_1

V_0,V_1=np.loadtxt('dati/seconda_parte/buoni.txt',unpack='true')
V_1=V_1/1000
V_0=V_0[6:]
V_1=V_1[6:]
popt=([1,0.054,0.1,0,10,0])
popt,pcov=curve_fit(funzione,V_0,V_1,absolute_sigma='false',maxfev=10000)


pylab.plot(V_0,V_1,'.')
x=np.linspace(V_0[0],V_0[-1])
pylab.plot(x,funzione(x,*popt))
pylab.show()