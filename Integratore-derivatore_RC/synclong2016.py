# Questo script serve per interfacciarsi con Arduino nell'esperienza
# dell'acquisizione sincrona di segnali
# L'interfacciamento avviene attraverso:
# 1. scrittura di un carattere (byte) che esprime l'intervallo di campionamento
# 2. lettura dei dati disponibili su porta seriale

import serial # libreria per gestione porta seriale (USB)
import time # libreria per temporizzazione

Directory='dati/'   # nome directory dati
                                                    # << DA CAMBIARE SECONDO NECESSITA'
FileName=(Directory+'150hz.txt')  # nome file << DA CAMBIARE SECONDO NECESSITA'


ard=serial.Serial('/dev/cu.usbmodemFD121',19200)  # apre porta seriale (occhio alla sintassi, dipende
                                # dal sistema operativo!)
time.sleep(2)   # aspetta due secondi per evitare casini

ard.write(b'5') # scrive il carattere per l'intervallo di campionamento
                # in unita' di 100 us << DA CAMBIARE A SECONDA DEI GUSTI
                # l'istruzione b indica che e' un byte (carattere ASCII)

time.sleep(1) # aspetta un secondo per evitare casini

outputFile = open(FileName, "w" ) # apre file dati carica per scrittura

print ("start")

for j in range (0,2): # loop acquisizioni multiple (sono 8 di default)

# loop lettura dati da seriale (256 punti)
    for i in range (0,256):
        data = ard.readline().decode('ascii') # legge il dato e lo decodifica
        if data:
            outputFile.write(data) # scrive i blocchi di dati
    print ("Part ",j+1," done")            

outputFile.close() # chiude il file dei dati di carica

ard.close() # chiude la comunicazione seriale con Arduino

print('end') # scrive sulla console che ha finito
