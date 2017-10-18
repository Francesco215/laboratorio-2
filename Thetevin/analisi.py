import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats

Caduta_potenziale=0.2 							#questo se la misura è a fondo scala
V_0=([4.97,0.01]) 										#differenza di potenziale misurata
Resistenze=([[20.9,22.3,30.6,32.8,33.1,322,670,6760,67300,689000,6.95*10**6],[0.1,0.1,0.1,0.1,1,1,10,100,1000,10**4],[21,22,30,33,330,650,6500,65000,650000,69*10**6]])							#[resistenza, errore digite (poi diventa quello vero)]
Intenzità=([[0.113,0.1098,0.0925,0.0913,0.870,0.01394,7.12*10**(-3),7.24*10**(-4)],[0.0001,0.0001,0.0001,0.0001,0.0001,10**(-5),10**(-5),10**(-6)],[0.2,0.2,0.2,0.2,0.2,0.02,0.02,0.002]])							#[misura,incertezza,fondo scala]
#Resistenza_amperometro=([,])

#trattamento errori resistenze

for i in range (0,len(Resistenze[0])):
	if(Resistenze[0][i]<200): Resistenze[1][i]=sqrt((Resistenze[0][i]*(8/100))**2+(Resistenze[1][i]*3)**2)
	if(Resistenze[0][i]>200 && Resistenze[0][i]<2*10**6): Resistenze[1][i]=sqrt((Resistenze[0][i]*(8/100))**2+(Resistenze[1][i])**2)
	if(Resistenze[0][i]<2*10**6): Resistenze[1][i]=sqrt((Resistenze[0][i]/10)**2+(Resistenze[1][i]*2)**2)

Rthetevin=Resistenze[0][0]*(V_0[0]-2.86)/2.86
print(Rthetevin)

#trattamento errori Voltaggio

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

"""




