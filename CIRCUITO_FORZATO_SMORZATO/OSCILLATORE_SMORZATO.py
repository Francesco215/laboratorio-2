from scipy.optimize import curve_fit, differential_evolution
import numpy as np
import matplotlib.pylab as plt
from uncertainties import ufloat

f, V_out, V_in=np.loadtxt('DATA.txt', unpack='true')
Amp=V_out/V_in
DV_out=np.sqrt((V_out*3/100)**2+0.01**2)
DV_in=np.sqrt((V_in*3/100)**2+0.01**2)
Df=4
print(DV_in)
DA=DV_out/V_in+DV_in*V_out/V_in**2
DA=DA

R=342
C=0.1e-6
r=40.1
L=0.5

C1=6.28*R*C
C2=6.28*(R+r)*C
C3=(6.28*np.sqrt(L*C))


'''
V_O=ufloat(V_out, DV_out)
V_I=ufloat(V_in, DV_in)
Amp_err=V_O/V_I
print('Ampiezze:')
print(Amp_err)
'''

def A(x, a, b, c):
	return((a*x)/np.sqrt((b*x)**2+(1-(x*c)**2)**2))

def sfasamento(x, a, c):
	return((1-(x*c)**2)/(a*x))

popt, pcov= curve_fit(A, f, Amp,(C1,C2,C3) , DA)
c1, c2, c3=popt
Dc1, Dc2, Dc3=np.sqrt(pcov.diagonal())
chi2=((Amp-A(f, c1, c2, c3))**2/(DA**2)).sum()/len(f)

print('PARAMETRI OTTIMALI:')
print('c1=%f+-%f' %(c1, Dc1))
print('c2=%f+-%f' %(c2, Dc2))
print('c3=%f+-%f' %(c3, Dc3))
print('chi2/ndof=%f' %chi2)

def costant(x, a, b):
	return(a*x+b)


#CALCOLO HMFW
freq=np.linspace(0, 1600, 1000)
AM=np.amax(A(freq, c1, c2, c3)) 
'''
amplitudes=A(freq, c1, c2, c3)
index=amplitudes.index(AM/2)           #valore massimo dell'ampiezza
FM=freq[index]      #valore della frequenza per massima ampiezza (risonanza)
print('Frequenza di risonanza=%f' %FM)
f_p, f_m=optimize.fsolve(A(x, c1, c2, c3)-AM/2)
'''

plt.figure(1)
plt.grid(color='gray')
plt.title('Oscillatore Forzato')
plt.subplot(211)
'''
plt.avxline(f_p)
plt.axvline(f_m)
plt.axvline(FM)
'''
plt.xlabel(r'$f[Hz]$')
plt.ylabel(r'$Amp$')
plt.errorbar(f, Amp, DA, Df, '.')
#print(len(f),len(A),len(Df),len(DA))
plt.plot(np.linspace(0, 1600, 1000), A(np.linspace(0, 1600, 1000), c1, c2, c3))
plt.plot(np.linspace(0, 1600, 1000), costant(np.linspace(0, 1600, 1000), 0, AM/2))
plt.subplot(212)
plt.plot(np.linspace(0, 1600, 1000), costant(np.linspace(0, 1600, 1000), 0, 0))
plt.plot(f,A(f, c1, c2, c3)-Amp,'.')
plt.figure(2)
plt.xlabel(r'$f[Hz]$')
plt.ylabel(r'$\tan(\phi)$')
plt.plot(np.linspace(1, 1600, 1000), sfasamento(np.linspace(0, 1600, 1000), c1, c3))
plt.show()
