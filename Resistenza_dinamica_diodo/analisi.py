from uncertainties import ufloat
from uncertainties import unumpy as unp
import numpy as np
R_b=ufloat(685,5)
R_a=ufloat(6.68e3,50)

Rth=1/(1/R_a + 1/R_b)

def erroreIntensità(intensità,risoluzione):
	if(intensità<0.02):
		return np.sqrt((intensità*(5/1000))**2+(risoluzione)**2)
	if(intensità>0.02 and intensità<2):
		return np.sqrt((intensità*(12/1000))**2+(risoluzione)**2)
	if(intensità>2):
		return np.sqrt((intensità*(2/100))**2+(risoluzione*5)**2)

def errVoltOscilloscopio(volt,risoluzione):
	return np.sqrt(risoluzione**2+(volt*(3/100))**2+risoluzione**2)

R=unp.uarray([6.5e3,3.3e3,650,330],[325,165,32.5,16.5])
I_q=unp.uarray([0.648,1.307,6.27,12.26],[0.003,0.006,0.03,0.06])/1000
V_g=unp.uarray([190e-3,888e-3,2.12,6.44],[6e-3,28e-3,0.06,0.21])
v_d=unp.uarray([2.06,4.98,3.24,5.54],[0.54,0.61,1.04,1.12])/1000


V_th=(V_g*R_b)/(R_a+R_b)
i_d=(V_th-v_d)/Rth
r_d=v_d/i_d
eta_vt=52e-3
r_d_att=eta_vt/I_q
r_dfasulla=(v_d*R_a*R_b)/(V_g*R_b - v_d*(R_a+R_b))
print(r_dfasulla)