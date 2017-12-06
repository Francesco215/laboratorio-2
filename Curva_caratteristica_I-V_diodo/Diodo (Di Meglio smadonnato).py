import numpy as np
import scipy.optimize as optimize
import pylab as plt

#DATI
V2, V1=np.loadtxt('dati/suca.txt', unpack='true')
R, DR=[680, 33]
I=(V2-V1)/R
DV=1
DI=2/R+(V2-V1)*DR/(R**2)

def Int(x, a, b,c):
	return a*(np.exp(x/b)-1)+c

popt, pcov=optimize.curve_fit(Int, V2, I, (10., 50.,0), sigma=DV)#, absolute_sigma='false')
I_0, nVt, c=popt
DI_0, DnVt, Dc=np.sqrt(pcov.diagonal())
corr=pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1])
chi2=(((I-Int(V2,*popt))/DI)**2).sum()/len(V2)

print('I_0(senza calibrazione)=%f+-%f' %(I_0, DI_0))
print('nVt(senza calibrazione)=%f+-%f' %(nVt, DnVt))
print('Correlazione (senza calib.)0%f' %corr)
print('Chi Quadro Normalizzato (senza calib.)=%f' %chi2)

def costant(x, a):
	return(a*x)

plt.figure(1)
plt.subplot(211)
plt.title('Shockley(no calibr.)')
plt.xlabel('DV[digit]')
plt.ylabel('I[digit/Ohm]')
plt.errorbar(V2, I, DI, DV, '.')
plt.plot(np.linspace(0, 790,10000), Int(np.linspace(0, 790,10000),*popt))
plt.subplot(212)
plt.plot(np.linspace(0, 290, 1000), costant(np.linspace(0, 290, 1000), 0))
plt.plot(I-Int(V2,*popt), 'o')
plt.show()

plt.figure(2)
plt.errorbar(V2, I, DI, DV)
plt.show()


#CALIBRAZIONE (da digit a volt senza offset)
#Vref, DVref=[;]      #presa con multimetro tra boccola rossa di arduino e linea di terra (boccola nera)
E, DE=[0.00477, 0.00029]    #per il momento uso risultati di vecchie misure, altrimenti E=Vref/1023
V1=V1*E
DV1=DV*E+V1*DE
V2=V2*E
DV2=DV1+E+V2*DE
I=(V2-V1)/R
DI=(DV1+DV2)/R+(V2-V1)*DR/(R**2)
punto=40
#p_0=([I[0],np.log(I[-1]/I[punto])/(V2[-1]-V2[punto]),0])
p_0=[I[0],(V2[-1]-V2[punto])/np.log(I[-1]/I[punto]),0]

popt, pcov=optimize.curve_fit(Int, V2, I, p_0, sigma=DI,maxfev=3000)#, absolute_sigma='false')
I_0, nVt, c=popt
DI_0, DnVt, Dc=np.sqrt(pcov.diagonal())
corr=pcov[0][1]/np.sqrt(pcov[0][0]*pcov[1][1])
chi2=(((I-Int(V2,*popt))/DI)**2).sum()/len(V2)

print('I_0(con calibrazione)=%f+-%f' %(I_0, DI_0))
print('nVt(con calibrazione)=%f+-%f' %(nVt, DnVt))
print('Correlazione (calib.)0%f' %corr)
print('Chi Quadro Normalizzato (senza calib.)=%f' %chi2)

def costant(x, a):
	return(a*x)

plt.figure(3)
plt.subplot(211)
plt.title('Shockley(con calibr.)')
plt.xlabel('DV[V]')
plt.ylabel('I[A]')
plt.errorbar(V2, I, DI, DV2, '.')
plt.plot(np.linspace(0, 3.5,10000), Int(np.linspace(0, 3.5,10000), *popt))
plt.subplot(212)
plt.plot(np.linspace(0, 290, 1000), costant(np.linspace(0, 290, 1000), 0))
plt.plot(I-Int(V2, *popt), 'o')
plt.show()


