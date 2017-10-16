import numpy as np
Resistenze=([[33.0,67.6,33.7*10**3,6.84*10**5,32.8*10**2],#misurate con il multimetro
			 [0.1,0.1,0.01*10**2,10**3,1],#errore multimetro
			 [33.0,65.0,33*10**3,33*10**5,32*10**2]])#cosa c'è scritto sopra
intenzità=([97.4*10**(-3),58.3*10**(-3),169.3*10**(-6),32.6*10**(-6),1.55*10**(-3),0.1,58*10**(-3),150*10**(-6),21*10**(-6),1.5*10**(-3)],
			[10**(-4),10**(-4),10**(-7),10*+(-5)],10**(-7),10**(-3),10**(-3),10**(-6),10**(-6),10**(-3))
DV=([3.2,4.0,5.0,5.1,5.0,3.2,3.9,5.0,5.0,4.9],[0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1])
RAnalogico=2*10**5
RDigitale=10**7

for i in range(5,len(intenzità[0])):
	#calcolo resistenza
	"""
	res=Resistenze[0][i%5]
	if i>4:
		Req=(res*RDigitale)/(res+RDigitale)
	else
		Req=(res*RAnalogico)/(res+RAnalogico)
"""

	Vatt=(Resistenze[0][i%5]*intenzità[0][i])
	dVatt=DV[1][i]/Resistenze[0][i%5]+(DV[0][i]*Resistenze[1][i%5])/Resistenze[0][i%5]**2


	print(Vatt, dVatt)
	#print(DV[0][i]/intenzità[0][i],Req,Req/(DV[0][i]/intenzità[0][i]))
