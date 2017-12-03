import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats

def sinusoide(tempo,amp,fase,sfase,omega):
	return amp*np.sin(omega*tempo+fase)+sfase

t, V=np.loadtxt('dati1.txt' , unpack='true')

