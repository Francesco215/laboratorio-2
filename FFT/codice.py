import numpy as np
import matplotlib.pyplot as plt

dati=['sinusoidelunga','triangolarelunga','575hZ','25hz','100hZ']
i=0
t,V=np.genfromtxt('dati/'+dati[i]+'.txt',unpack='true')
t=t*1e-6
dt=t[4]-t[3]
Fv=np.abs(np.fft.rfft(V))[1:-2]#taglio i valori associati a frequenze minori o uguali a zero
freq=np.fft.fftfreq(len(t),dt)[2:len(Fv)+2]#levo le frequaenze minori o uguali a zero

plt.figure()
plt.subplot(211)
plt.plot(t,V)
plt.title("Segnale Arduino")
plt.xlabel("Tempo [s]")
plt.ylabel("ddp [V]")#plotto i dati
plt.xlim(0,0.05)

plt.subplots_adjust(hspace=0.5)

plt.subplot(212)
plt.yscale('log')
print(freq)
print(len(freq),len(Fv))
plt.plot(freq,Fv)#plotto la trasformata
plt.title("Trasformata")
plt.xlabel("Frequenza [Hz]")
plt.ylabel("spettro")

plt.savefig('grafici/'+dati[i]+'.png')
#plt.show()