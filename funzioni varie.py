import numpy as np
import pylab
from scipy.optimize import curve_fit
from scipy import stats

def erroreResistenze(resistenza,risoluzione):
	if(resistenza<200):
		return np.sqrt((resistenza*(8/1000))**2+(risoluzione*3)**2)
	if(resistenza>200 and resistenza<2*10**6):
		return np.sqrt((resistenza*(8/1000))**2+(risoluzione)**2)
	if(resistenza<2*10**6):
		return np.sqrt((resistenza/100)**2+(risoluzione*2)**2)

def erroreIntensità(intensità,risoluzione):
	if(intensità<0.02):
		return np.sqrt((intensità*(5/1000))**2+(risoluzione)**2)
	if(intensità>0.02 and intensità<2):
		return np.sqrt((intensità*(12/1000))**2+(risoluzione)**2)
	if(intensità>2):
		return np.sqrt((intensità*(2/100))**2+(risoluzione*5)**2)

def errVoltOscilloscopio(volt,risoluzione):
	return np.sqrt(risoluzione**2+(volt*(3/100))**2+risoluzione**2)

def errFreqOscilloscopio(freq,risoluzione):
	return np.sqrt(risoluzione**2+(freq/100)**2)

def RicercaMaxMin(y):
	massimi=np.array([])
	minimi=np.array([])
	for i in range(2,len(y)):
		if y[i-2]<y[i-1] and y[i]<y[i-1]: np.append(massimi,i-1)
		if y[i-2]>y[i-1] and y[i]>y[i-1]: np.append(minimi,i-1)
	return massimi.astype(int),minimi.astype(int)
