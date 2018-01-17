import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

def shock(V, I0, nVt) :
    return I0*(np.exp(V/nVt)-1)
    
def derivata(V, I0, nVt) :
    return (I0/nVt)*np.exp(V/nVt)

V1_digit, V2_digit = np.genfromtxt("losifra4diodo.txt", unpack=True)

Vref = 4.93    # Da cambiare
dVref = 0.03
Rd = 3280
dRd = 30
X = Vref/1023
dX = dVref/1023

V1 = V1_digit*X
dV1 = X*1 + V1*dX
V2 = V2_digit*X
dV2 = X*1 + V2*dX

I = ((V1-V2)/Rd)*1000
dI = ((dV1+dV2)/Rd + (V1-V2)*dRd/(Rd**2))*1000

ndof = len(V1)-2
dI_eff = dI
val = (1, 0.05)
for i in range(10):
    popt, pcov = scipy.optimize.curve_fit(shock, V2, I, val, dI_eff, absolute_sigma = False)
    chi_2 = np.sum(((I - shock(V2,*popt))/dI_eff)**2)
    print(chi_2)
    dI_eff = np.sqrt(((derivata(V2,*popt))*dV2)**2 + dI**2)

V2_out = np.array([])
I_out = np.array([])
dI_eff_out = np.array([])
differenza = (I-shock(V2, *popt))/dI_eff
for i in range(len(V2)) :
    if(abs(differenza[i])<1) :
        V2_out = np.append(V2_out, V2[i])
        I_out = np.append(I_out, I[i])
        dI_eff_out = np.append(dI_eff_out, dI_eff[i])

print("\nPORCODDIO RICORDA DI METTERE LA CAZZO DI ABS_SIGMA CHE CE LA SCORDIAMO SEMPRE... PORCA MADONNA\n")
print("chi2/ndof =",chi_2,"/",ndof,"=",chi_2/ndof)
print("I0=", popt[0], "+-", pcov[0][0]**0.5)
print("nVt=", popt[1], "+-", pcov[1][1]**0.5)
print("Cov normalizzata", pcov[1][0]/(pcov[0][0]*pcov[1][1])**0.5, "\n")
print("chi2 senza outliers", np.sum(((I_out - shock(V2_out,*popt))/dI_eff_out)**2), "ndof", len(I_out)-2)
print("\nPORCODDIO RICORDA DI METTERE LA CAZZO DI ABS_SIGMA CHE CE LA SCORDIAMO SEMPRE... PORCA MADONNA\n")

t = np.linspace(0, 0.63, 4000)
plt.figure()
plt.subplot(211)
plt.title("Grafico I-V diodo")
plt.xlabel("ddp [V]")
plt.ylabel("I [mA]")
plt.errorbar(V2, I, dI, dV2, fmt = '.', label = "Data")
plt.plot(t, shock(t,*popt), label = "Fit")
plt.legend()

plt.subplot(212)
plt.title("Residui normalizzati")
plt.xlabel("ddp [V]")
plt.errorbar(V2_out, (I_out-shock(V2_out, *popt))/dI_eff_out, fmt=".")
plt.plot(t, t*0)
plt.show()