import numpy as np
import pylab
from uncertainties import ufloat
from uncertainties import unumpy as unp

def erroreResistenze(resistenza,risoluzione):
	if(resistenza<200):
		return np.sqrt((resistenza*(8/1000))**2+(risoluzione*3)**2)
	if(resistenza>200 and resistenza<2*10**6):
		return np.sqrt((resistenza*(8/1000))**2+(risoluzione)**2)
	if(resistenza<2*10**6):
		return np.sqrt((resistenza/100)**2+(risoluzione*2)**2)

#dati=['004','025','068','105','122','149','174','212']#*10^-7 Ampere
dati=['025']
R=([1.005e3,erroreResistenze(1.005e3,1)])
Vref=(4.89/1023)
#4.89:1023=V:digit

for i in range (0,len(dati)):
	V1,V2=np.loadtxt('dati_e-7_ampere/'+dati[i]+'.txt',unpack='true')*Vref
	I=[(V1-V2)/R[0],((V1-V2)*R[1] + R[0]*2*Vref)/(R[0])**2]
	V1=[V1,V1*Vref]
	V2=[V2,V2*Vref]
	pylab.errorbar(V2[0],I[0],yerr=I[1])
#pylab.savefig('figura1.png')
pylab.show()

a=unp.uarray([2.57,10.5,17.4,21.2],[0.01,0.05,0.08,0.11])
b=unp.uarray([0.26,1.31,2.23,2.75],[0.02,0.02,0.03,0.03])

print(b/a)