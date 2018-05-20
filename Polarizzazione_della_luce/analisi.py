from uncertainties import unumpy as unp
from uncertainties import ufloat
import numpy as np
import pylab as pb
from scipy.optimize import curve_fit

def erroreIntensità(intensità,risoluzione):
	if(intensità<0.02):
		return np.sqrt((intensità*(5/1000))**2+(risoluzione)**2)
	if(intensità>0.02 and intensità<2):
		return np.sqrt((intensità*(12/1000))**2+(risoluzione)**2)
	if(intensità>2):
		return np.sqrt((intensità*(2/100))**2+(risoluzione*5)**2)

#punto 1 e 2
mu=4*np.pi*(10**(-7))
c=299792458 
A=7.5e-6
lambd=ufloat(655e-9,25e-9)
f=c/lambd
h=6.626070040e-34
Iph=ufloat(111.08e-6,erroreIntensità(111.08e-6,1e-8))

P=Iph/0.4
E0=unp.sqrt(2*Iph*mu*c/(A*0.4))
phi=Iph/(h*f*0.4)

#punto3
I=np.loadtxt('tabella1.txt', unpack='true')
I=I*10**(-6)
Ierr=[]
errori=open('err1.txt','w')
for i in range (0,len(I)):
	if i<18 and i>12:
		err=erroreIntensità(I[i],1e-8)
	else:
		err=erroreIntensità(I[i],1e-7)
	errori.write("%s\n" % err)

#punto5
I=np.loadtxt('tabella2.txt', unpack='true')
I=I*10**(-6)
Ierr=[]
errori=open('err2.txt','w')
for i in range (0,len(I)):
	err=erroreIntensità(I[i],1e-8)
	errori.write("%s\n" % err)
