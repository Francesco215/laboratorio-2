#1 microfarad e
import numpy as np
import pylab
from scipy.optimize import curve_fit

t,x=pylab.loadtxt('dati/150hz.txt',unpack='true')
print (t,x)
pylab.plot(t,x)
pylab.show()