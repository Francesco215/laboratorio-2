import numpy as np
import scipy.optimize as optimize
import pylab as plt
from uncertainties import ufloat

V_out, V_in, f=np.loadtxt('', unpack='true')
Amp=V_out/V_in
DA=DV/V_in+DV*V_out/V_in**2
DV, Df=(,)
V_O=ufloat(V_out, DV)
V_I=ufloat(V_in, DV)
Amp_err=V_O/V_I
print('Ampiezze:')
print(Amp_err)

def A(x, a, b, c):
	return(a*x/np.sqrt((b*x)**2+(1-(c*x)**2)**2))

def sfasamento(x, a, c):
	return((1-(c*x)**2)/(a*x))

popt, pcov= optimize.curve_fit(A, f, Amp, (, ,), DA)
c1, c2, c3=popt
Dc1, Dc2, Dc3=np.sqrt(pcov.diagonal())
chi2=((Amp-A(f, c1, c2, c3))**2/(Df**2)).sum()/len(f)

print('PARAMETRI OTTIMALI:')
print('c1=%f+-%f' %(c1, Dc1))
print('c2=%f+-%f' %(c2, Dc2))
print('c3=%f+-%f' %(C3, Dc3))
print('chi2/ndof=%f' %chi2)

def costant(x, a):
	return(a*x)

plt.figure(1)
plt.subplot(211)
plt.errorbar(f, V, Df, DV, '+')
plt.plot(np.linspace(0, 100, 1000), A(np.linspace(0, 100, 1000), c1, c2, c3))
plt.subplot(212)
plt.plot(np.linspace(1, 100, 1000), sfasamento(np.linspace(0, 100, 1000), c1, c3))
plt.subplot(213)
plt.plot(np.linspace(0, 100, 1000), costant(np.linspace(0, 100, 1000), 0))
plt. plot(A(f, c1, c2, c3)-Amp)



