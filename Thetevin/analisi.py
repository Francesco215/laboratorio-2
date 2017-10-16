import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats

Caduta_potenziale=0.2 							#questo se la misura è a fondo scala
V_0=([,]) 										#differenza di potenziale misurata
Resistenze=([[],[]])							#[resistenza, errore digite (poi diventa quello vero)]
Intenzità=([[],[],[]])							#[misura,incertezza,fondo scala]
Resistenza_amperometro=([,])

for i in range (0,len(Resistenze[0])):
	if(Resistenze[0][i]<200): Resistenze[1][i]=sqrt((Resistenze[0][i]*(8/100))**2+(Resistenze[1][i]*3)**2)
	if(Resistenze[0][i]>200 && Resistenze[0][i]<2*10**6): Resistenze[1][i]=sqrt((Resistenze[0][i]*(8/100))**2+(Resistenze[1][i])**2)
	if(Resistenze[0][i]<2*10**6): Resistenze[1][i]=sqrt((Resistenze[0][i]/10)**2+(Resistenze[1][i]*2)**2)

for i in range (0,len(Intenzità[2])):
	Resistenza_amperometro[i]=Caduta_potenziale/Intenzità[2][i]

def fit(resistenza,resistenza_generatore,Vo):
	Return Vo/(resistenza+resistenza_generatore)

popt,pcov=curve_fit(fit,Resistenze[0]+Resistenza_amperometro,Intenzità[0],sigma=Intenzità[1],absolute_sigma=false)

for i in range (0,len(Resistenze[0])):
	chi2=chi2+((Intenzità[0][i]-fit(Resistenze[0][i]+Resistenza_amperometro,*popt))/Intenzità[1][i])**2

chi2_n=chi2/len(Resistenze[0])

def grafico(x,y,errY,cos):
	Xmax=np.amax(x)
	Xmin=np.amin(x)
	Ymax=np.amax(y)
	Ymin=np.amin(y)
	pylab.xlim(Xmin-(Xmax-Xmin)/cos,Xmax+(Xmax-Xmin)/cos)
	pylab.ylim(Ymin-(Ymax-Ymin)/cos,Ymax+(Ymax-Ymin)/cos)
	pylab.errorbar(x,y,errY,linestyle='',color='black',marker='o')

grafico(Resistenze[0],Intenzità[0],Intenzità[1],15)
pylab.xscale('log')
pylab.yscale('log')

pylab.errorbar(Resistenze[0],Intenzità[0],Intenzità[1],linestyle='',color='black',marker='o')






