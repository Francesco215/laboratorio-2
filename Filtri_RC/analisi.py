import numpy as np
import pylab
from scipy.optimize import curve_fit
from scipy import stats
Vin=20.4
## 1/RC è definita come frequenza di taglio

frequenza, Vout, deltaT=np.loadtxt('dati.txt', unpack='true')

def Attenuazione(volt,risoluzione):
	errVout=np.sqrt(risoluzione**2+(volt*(3/100))**2)
	errVin=np.sqrt(risoluzione**2+(Vin*(3/100))**2)
	errAtt=(volt/Vin)*(errVout/Vin + (volt*errVin)/Vin**2)
	return volt/Vin, errAtt

def errFreqOscilloscopio(freq,risoluzione):
	return np.sqrt(risoluzione**2+(freq/100)**2)

def fAttenuazione(frequenza,a,freqTaglio):
	return a/np.sqrt(1+(frequenza/freqTaglio)**2)

def dAttenuazione(frequenza,a,freqTaglio):
	return (2*a*frequenza)/(freqTaglio*(1+(frequenza/freqTaglio)**2)**(3/2))

digitF=np.array([])
for i in range (0,len(frequenza)):
	for j in range (-10,5):
		if frequenza[j]<10**j:
			digitF=np.insert(digitF,len(digitF),j-2)
			break

attenuazione=Attenuazione(Vout,0.08)
errFreq=errFreqOscilloscopio(frequenza,digitF)

popt,pcov=curve_fit(fAttenuazione, frequenza, attenuazione[0], sigma=attenuazione[1], absolute_sigma='false')

for i in range(0,20):
	err=np.sqrt((dAttenuazione(frequenza,*popt)*errFreq)**2+attenuazione[1]**2)
	popt,pcov=curve_fit(fAttenuazione, frequenza, attenuazione[0], sigma=err, absolute_sigma='false')
chi2=0


for i in range(0,len(frequenza)):
	chi2=chi2+((attenuazione[0][i]-fAttenuazione(frequenza[i],*popt))/err[i])**2
	print((deltaT[i]*frequenza[i])/500)


pylab.errorbar(frequenza,attenuazione[0],attenuazione[1],errFreq,'.')
x=np.exp(np.linspace(3,8.5,100))
y=fAttenuazione(x,*popt)
pylab.plot(x,y)
pylab.xscale('log')
pylab.yscale('log')
pylab.xlabel('frequenza')
pylab.ylabel('attenuazione')
pylab.show()
