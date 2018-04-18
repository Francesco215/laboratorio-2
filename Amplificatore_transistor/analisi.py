from uncertainties import ufloat
from uncertainties import unumpy as unp
import pylab
import numpy as np

def erroreIntensità(intensità,risoluzione):
	if(intensità<0.02):
		return np.sqrt((intensità*(5/1000))**2+(risoluzione)**2)
	if(intensità>0.02 and intensità<2):
		return np.sqrt((intensità*(12/1000))**2+(risoluzione)**2)
	if(intensità>2):
		return np.sqrt((intensità*(2/100))**2+(risoluzione*5)**2)

verroreIntensità=np.vectorize(erroreIntensità)

def errVoltOscilloscopio(volt,risoluzione,spessore):
	return np.sqrt(risoluzione**2+(volt*(3/100))**2+risoluzione**2+spessore**2)

verrVoltOscilloscopio=np.vectorize(errVoltOscilloscopio)
Vin=[1.28e-3,0.61e-3]
err=[0.28e-3,0.16e-3]
ris=[0.01e-3,0.01e-3]
Vin=unp.uarray(Vin,verrVoltOscilloscopio(Vin,ris,err))
Vout=[35.8e-3,36.2e-3]
err=[0.8e-3,0.8e-3]
ris=[0,0]
Vout=unp.uarray(Vout,verrVoltOscilloscopio(Vout,ris,err))


Ic=[5.27e-3,5.24e-3,0.95e-3,0.336e-3,25.1e-6]
ris=[0.01e-3,0.01e-3,0.01e-3,0.001e-3,0.1e-6]
Ic=unp.uarray(Ic,verroreIntensità(Ic,ris))
Ib=unp.uarray([6e-3,120e-6,12e-6,6e-6,1.2e-6],[1e-3,10e-6,1e-6,1e-6,1e-6])



Vin=[7.6e-3,3.92e-3]
ris=[0.8e-3,0.08e-3]
err=[0,0]
Vout=[16.20e-3,15.80e-3]

Vin=unp.uarray(Vin,verrVoltOscilloscopio(Vin,ris,err))
Vout=unp.uarray(Vout,verrVoltOscilloscopio(Vout,ris,err))

Vbe=[1.02,0.736,0.616,0.592,0.520]
ris=[0.02,0.008,0.008,0.008,0.008]
err=[0,0,0,0,0]
Vbe=unp.uarray(Vbe,verrVoltOscilloscopio(Vbe,ris,err))

print(Vbe)

