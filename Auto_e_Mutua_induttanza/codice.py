from uncertainties import unumpy as unp
from uncertainties import ufloat
import numpy as np

R=ufloat(3480,3)
r=ufloat(40.3,0.3)
Ft=ufloat(105.2,10.7)

A=(R+r)/(2*np.pi*Ft*np.sqrt(2))

Vi=ufloat(4.88,0.08)
Vr=unp.uarray([0.416,1.60,0.92],[0.008,0.04,0.04])
A=Vr/Vi
f=ufloat(1520,10)


V2=ufloat(0.60,0.01)
VR=ufloat(0.76,0.02)
f=ufloat(1785,1)
A=VR/V2
L=R/(2*np.pi*f*A)
M=(R*V2)/(2*np.pi*f*VR)



V1=ufloat(4.88,0.8)

Vi=ufloat(11.12,0.03)
Vr=ufloat(5.74,0.02)
A=Vr/Vi
f=ufloat(10310,10)
L=(R)/(2*np.pi*f*A)
L1=0.25
L2=0.14


R=ufloat(342,3)
V2=ufloat(0.60,0.01)
VR=ufloat(0.76,0.02)
f=ufloat(1785,1)
A=Vr/Vi
L=R/(2*np.pi*f*A)


print(L)




