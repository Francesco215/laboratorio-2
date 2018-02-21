import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

def shock(V, I0, nVt) :
    return I0*(np.exp(V/nVt)-1)
    
def derivata(V, I0, nVt) :
    return (I0/nVt)*np.exp(V/nVt)

freq_treno, V_lum = np.genfromtxt("dati/seconda_parte/pollice.txt", unpack=True, skip_header=3)

V_lum[:8] += 0.007
V_lum[-10:] += -0.001
Vref = 5.08    # Da cambiare
dVref = 0.03
Rd = 371
dRd = 5
X = Vref/255
dX = dVref/255

V1 = freq_treno*X
dV1 = X*2 + freq_treno*dX
dV_lum = V_lum/100

I = ((V1-V_lum)/Rd)*1000
dI = ((dV1+dV_lum)/Rd + (V1-V_lum)*dRd/(Rd**2))*1000

ndof = len(V1)-2
dI_eff = dI
val = (1, 0.05)
for i in range(10):
    popt, pcov = scipy.optimize.curve_fit(shock, V_lum, I, val, dI_eff, absolute_sigma = False)
    chi_2 = np.sum(((I - shock(V_lum,*popt))/dI_eff)**2)
    print(chi_2)
    dI_eff = np.sqrt(((derivata(V_lum,*popt))*dV_lum)**2 + dI**2)

V_lum_out = np.array([])
I_out = np.array([])
dI_eff_out = np.array([])
differenza = (I-shock(V_lum, *popt))/dI_eff
for i in range(len(V_lum)) :
    if(abs(differenza[i])<1) :
        V_lum_out = np.append(V_lum_out, V_lum[i])
        I_out = np.append(I_out, I[i])
        dI_eff_out = np.append(dI_eff_out, dI_eff[i])

print("\nPORCODDIO RICORDA DI METTERE LA CAZZO DI ABS_SIGMA CHE CE LA SCORDIAMO SEMPRE... PORCA MADONNA\n")
print("chi2/ndof =",chi_2,"/",ndof,"=",chi_2/ndof)
print("I0=", popt[0], "+-", pcov[0][0]**0.5)
print("nVt=", popt[1], "+-", pcov[1][1]**0.5)
print("Cov normalizzata", pcov[1][0]/(pcov[0][0]*pcov[1][1])**0.5, "\n")
print("chi2 senza outliers", np.sum(((I_out - shock(V_lum_out,*popt))/dI_eff_out)**2), "ndof", len(I_out)-2)
print("\nPORCODDIO RICORDA DI METTERE LA CAZZO DI ABS_SIGMA CHE CE LA SCORDIAMO SEMPRE... PORCA MADONNA\n")

t = np.linspace(0, 0.35, 4000)
plt.figure()
plt.subplot(211)
plt.title("Grafico I-V diodo")
plt.xlabel("ddp [V]")
plt.ylabel("I [mA]")
plt.errorbar(V_lum, I, dI, dV_lum, fmt = '.', label = "Data")
plt.plot(t, shock(t,*popt), label = "Fit", color = 'red')
#plt.legend()

plt.subplot(212)
plt.title("Residui normalizzati")
plt.xlabel("ddp [V]")
plt.errorbar(V_lum_out, (I_out-shock(V_lum_out, *popt))/dI_eff_out, fmt=".")
plt.plot(t, t*0, color = 'red')
plt.show()