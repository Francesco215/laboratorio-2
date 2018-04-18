# Questo script serve per interfacciarsi con Arduino nell'esperienza
# dell'oscillatore rLC smorzato con modalita' di acquisizione interleaved

# L'interfacciamento avviene attraverso:
# 1. scrittura di un carattere (byte) che esprime l'intervallo di campionamento
# 2. lettura dei dati disponibili su porta seriale

import serial # libreria per gestione porta seriale (USB)
import time # libreria per temporizzazione
import numpy
import pylab


Directory='../dati_arduino/'   # nome directory dati
                                                    # << DA CAMBIARE SECONDO NECESSITA'
FileName=Directory+'datint.txt'  # parte comune nome file << DA CAMBIARE SECONDO NECESSITA'


ard=serial.Serial('/dev/ttyACM0',19200)   # apre porta seriale (occhio alla sintassi, dipende
                                # dal sistema operativo!)
time.sleep(2)   # aspetta due secondi per evitare casini

ard.write(b'5') # scrive il carattere per l'intervallo di campionamento
                # in unita' di 10 us << SI CONSIGLIA DI NON CAMBIARE
                # l'istruzione b indica che e' un byte (carattere ASCII)

time.sleep(1) # aspetta un secondo per evitare casini

outputFile = open(FileName, "w" ) # apre file dati carica per scrittura

print ("start")
# loop lettura dati da seriale (256 punti)

for j in range (0,8):
    for i in range (0,256):
        data = ard.readline().decode() # legge il dato e lo decodifica
        if data:
            outputFile.write(data) # scrive blocchi da 256 in file
            
    print ("Part ",j+1,"of 8 done")


ard.close() # chiude la comunicazione seriale con Arduino

        
outputFile.close() # chiude il file dei dati

print('end') # scrive sulla console che ha finito
