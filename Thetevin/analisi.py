import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats

Caduta_potenziale=0.2 							#questo se la misura è a fondo scala
V_0=([4.97,0.01]) 										#differenza di potenziale misurata
Resistenze=([[20.9,22.3,30.6,32.8,33.1,322,670,6760,67300,689000,6.95*10**6],
			[0.1,0.1,0.1,0.1,0.1,1,1,10,100,1000,10**4],
			[21,22,30,33,330,650,6500,65000,650000,69*10**6]])							#[resistenza, errore digite (poi diventa quello vero)]
Intenzità=np.array([[0.113,0.1098,0.0925,0.0913,0.087,0.01394,7.12*10**(-3),7.24*10**(-4),73*10**(-6),7.14*10**(-6),7.1*10**(-7)],
			[0.0001,0.0001,0.0001,0.0001,0.0001,10**(-5),10**(-5),10**(-6),10**(-7),10**(-8),10**(-8)],
			[0.2,0.2,0.2,0.2,0.2,0.02,0.02,0.002,0.0002,2*10**(-5),2*10**(-5)]])							#[misura,incertezza,fondo scala]
Resistenza_amperometro=np.array([])

#trattamento errori resistenze

for i in range (0,len(Resistenze[0])):
	if(Resistenze[0][i]<200):
		Resistenze[1][i]=np.sqrt((Resistenze[0][i]*(8/1000))**2+(Resistenze[1][i]*3)**2)
	if(Resistenze[0][i]>200 and Resistenze[0][i]<2*10**6):
		Resistenze[1][i]=np.sqrt((Resistenze[0][i]*(8/1000))**2+(Resistenze[1][i])**2)
	if(Resistenze[0][i]<2*10**6):
		Resistenze[1][i]=np.sqrt((Resistenze[0][i]/100)**2+(Resistenze[1][i]*2)**2)

for i in range(0,len(Intenzità[0])):
	if(Intenzità[0][i]<0.02):
		Intenzità[1][i]=np.sqrt((Intenzità[0][i]*(5/1000))**2+(Intenzità[1][i])**2)
	if(Intenzità[0][i]>0.02 and Intenzità[0][i]<2):
		Intenzità[1][i]=np.sqrt((Intenzità[0][i]*(12/1000))**2+(Intenzità[1][i])**2)
	if(Intenzità[0][i]>2):
		Intenzità[1][i]=np.sqrt((Intenzità[0][i]*(2/100))**2+(Intenzità[1][i]*5)**2)

Rthetevin=Resistenze[0][4]*(V_0[0]-2.86)/2.86

#trattamento errori Voltaggio

for i in range (0,len(Intenzità[2])):
	Resistenza_amperometro=np.insert(Resistenza_amperometro,len(Resistenza_amperometro),Caduta_potenziale/Intenzità[2][i])

def fit(resistenza,resistenza_generatore,Vo):
	return Vo/(resistenza+resistenza_generatore)
def dfit(resistenza,resistenza_generatore,Vo):
	return Vo/(resistenza+resistenza_generatore)**2
vfit=np.vectorize(fit)
vdfit=np.vectorize(dfit)

popt,pcov=curve_fit(fit,Resistenze[0]+Resistenza_amperometro,Intenzità[0],sigma=Intenzità[1],absolute_sigma='false')
ErroriEff=Intenzità[1]
for i in range(0,40):
	for i in range(0,len(Resistenze)):
		ErroriEff[i]=np.sqrt((Resistenze[1][i]*dfit(Resistenze[0][i],*popt))**2+Intenzità[1][i]**2)
	popt,pcov=curve_fit(fit,Resistenze[0]+Resistenza_amperometro,Intenzità[0],sigma=ErroriEff,absolute_sigma='false')

#print(popt,np.sqrt(pcov.diagonal()))
chi2=0.
for i in range (0,len(Resistenze[0])):
	chi2=chi2+((Intenzità[0][i]-fit(Resistenze[0][i]+Resistenza_amperometro[i],*popt))/Intenzità[1][i])**2

chi2_n=chi2/len(Resistenze[0])
print(pcov[1][0]/np.sqrt(pcov[0][0]*pcov[1][1]))


def grafico(x,y,errY,cos):
	Xmax=np.amax(x)
	Xmin=np.amin(x)
	Ymax=np.amax(y)
	Ymin=np.amin(y)
	#pylab.xlim(Xmin-(Xmax-Xmin)/cos,Xmax+(Xmax-Xmin)/cos)
	#pylab.ylim(Ymin-(Ymax-Ymin)/cos,Ymax+(Ymax-Ymin)/cos)
	pylab.errorbar(x,y,errY,linestyle='',color='black',marker='o')


x=np.linspace(Resistenze[0][0],Resistenze[0][len(Resistenze[0])-1],10**6)
y=vfit(x,*popt)
pylab.plot(x,y)
#grafico(Resistenze[0]+Resistenza_amperometro,Intenzità[0],Intenzità[1],15)

pylab.xscale('log')
pylab.yscale('log')
pylab.xlabel('Resistenza [Ω]')
pylab.ylabel('Intenzità [A]')
pylab.errorbar(Resistenze[0],Intenzità[0],Intenzità[1],linestyle='',color='black',marker='.')
pylab.show()

def zero(x,a):
	return a*x

x=np.linspace(Resistenze[0][0],Resistenze[0][len(Resistenze[0])-1],20)
y=zero(x,0)
pylab.plot(x,y)
pylab.xscale('log')
pylab.xlabel('Resistenza [Ω]')
pylab.ylabel('Residui Intenzità [A]')
pylab.errorbar(Resistenze[0],Intenzità[0]-vfit(Resistenze[0],*popt),Intenzità[1],linestyle='',color='black',marker='.')
pylab.show()

