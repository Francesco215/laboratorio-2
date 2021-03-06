import numpy as np
import pylab as plt
import scipy.optimize as optimize
import scipy.stats as stats
from scipy.odr import odrpack

t, V=np.loadtxt('dati1.txt' , unpack='true')
Dt, DV=(4, 1)

#ONDA SINUSOUISALE      :i dati vengono sbagliati (non so ancora il perchè)
def  Wave(x, a, b, w, d):
    return(a*np.cos(w*x+b)+d)

  
popt, pcov=optimize.curve_fit(Wave, t, V, (400, 157e-6, 3, 600), sigma=DV, absolute_sigma='false')

Vz, phi, w, offset=popt
DVz, Dphi, Dw, Doffset=np.sqrt(pcov.diagonal())
print('v_0=%f+-%f' %(Vz, DVz))
print('Sfasamento=%f+-%f' %(phi, Dphi))
print('Omega=%f+-%f' %(w, Dw))
print('Costante di Offset=%f+-%f' %(offset, Doffset))

chi2_norm=((V-Wave(t, Vz, phi, w, offset))**2/(DV)**2).sum()/(len(V-3))

print('Chi Quadro Normalizzato=%f' %chi2_norm)
'''


#PROVA CON ODR      :funziona alla perfezione
def Wave1(A, x):
    return(A[0]*np.cos(A[1]*x+A[2])+A[3])
    
model=odrpack.Model(Wave1)
data=odrpack.RealData(t, V, sx=Dt, sy=DV)
odr=odrpack.ODR(data, model, beta0=(400, 157e-6, 3, 600))
out=odr.run()
popt, pcov=out.beta, out.cov_beta
Vz, w, phi, offset=popt
DVz, Dw, Dphi, Doffset=np.sqrt(pcov.diagonal())
chi2=out.sum_square
chi2_norm=chi2/(len(V)-4)
print('V_0 odr=%f+-%f' %(Vz, DVz))
print('Omega odr=%f+-%f' %(w, Dw))
print('Sfasamento odr=%f+-%f' %(phi, Dphi))
print('Offset odr=%f+-%f' %(offset, Doffset))
print('Chi Quadro normalizzato=%f' %chi2_norm)
'''
corr=np.corrcoef(pcov)
#MATRICE DI CORRELAZIONE     :ottenuta partendo da quella di covarianza
for i in range(0, 3):
    for j in range(0, 3):
        corr[i][j]=pcov[i][j]/np.sqrt(pcov[i][i]*pcov[j][j])
        
print('Matrice di correlazione:')      #◘stampata integralmente
print(corr)

def costant(x, a):        #per fare la linea dritta nel grafico degli scarti
    return(a*x)
    
plt.figure(1)
plt.subplot(211)
plt.title('Wave Generator')
plt.xlabel('Time[us]')
plt.ylabel('DV[digit]')
plt.errorbar(t, V, Dt, DV, '.')
plt.plot(np.linspace(0, 140000, 30000), Wave(np.linspace(0, 140000, 30000), Vz, phi, w, offset))
plt.subplot(212)
plt.plot((V-Wave(t, Vz, w, phi, offset))/DV/1000)
plt.plot(np.linspace(0, 254, 1000), costant(np.linspace(0, 254, 1000), 0))
plt.show()

plt.figure(2)
plt.plot(t, V)
plt.show()