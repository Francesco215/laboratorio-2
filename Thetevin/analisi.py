import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats

Caduta_potenziale=0.2 #questo se la misura è a fondo scala
V_0=([val,err]) #differenza di potenziale misurata
Resistenze=([[],[]])#[resistenza,errore]
Intenzità=([[],[],[]])#[misura,incertezza,fondo scala]

def Res_int(intenzità,fondo_scala):
	return Caduta_potenziale*intenzità/fondo_scala

