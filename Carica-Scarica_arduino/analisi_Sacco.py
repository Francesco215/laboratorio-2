import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats


#legge il file e ritorna 2 vettori: il primo è quello delle potenziale, e il secondo è quello dei tempi
def lettura(file):
	potenziale,tempo=loadtxt(file,unpack=True)
	Potenziale=np.array([])
	Tempo=np.array([])
	for i in range(6,len(numero),4):
		Potenziale=np.insert(Potenziale,len(Potenziale),potenziale)
		Tempo=np.insert(Tempo,len(Tempo),tempo)
	return Potenziale,Tempo

