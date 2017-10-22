# Questo script serve per interfacciarsi con Arduino nell'esperienza
# di misura di d.d.p. continue

# L'interfacciamento avviene attraverso:
# 1. scrittura di un carattere (byte) che esprime l'intervallo di campionamento 
# 2. lettura dei dati disponibili su porta seriale

# L'operazione puo' essere ripetuta in loop

import serial # libreria per gestione porta seriale (USB)
import time # libreria per temporizzazione
import numpy

nacqs = 8 # numero di acquisizioni da registrare (ognuna da 256 coppie di punti)

Directory='../dati_arduino/'   # nome directory dati
                                                    # << DA CAMBIARE SECONDO NECESSITA'

FileName=Directory+'dati6.txt'  # parte comune nome file << DA CAMBIARE SECONDO NECESSITA'

outputFile = open(FileName, "w" ) # apre file dati predisposto per scrittura

print('Please wait')

for j in range (1,nacqs+1):

    
    ard=serial.Serial('/dev/ttyACM0',19200)  # apre porta seriale (occhio alla sintassi, dipende
                                    # dal sistema operativo!)
    print('Start Acquisition ',j, ' of ',nacqs) # scrive sulla console (terminale)
    time.sleep(2)   # aspetta due secondi per evitare casini
    
    ard.write(b'7') # scrive il carattere per l'intervallo di campionamento
                    # in unita' di 100 us << DA CAMBIARE A SECONDA DEI GUSTI
                    # l'istruzione b indica che e' un byte (carattere ASCII)
    
    time.sleep(2) # aspetta due secondi per evitare casini
        
   
   
    # loop lettura dati da seriale (256 coppie di dati: tempo in us, valore digitalizzato di d.d.p.)
    runningddp=numpy.zeros(256) # prepara il vettore per la determinazione della ddp media e std
    
    for i in range (0,256):
        data = ard.readline().decode() # legge il dato e lo decodifica
        if data:
            outputFile.write(data) # scrive i dati sul file
            runningddp[i]=data[data.find(' '):len(data)] # estrae le ddp e le mette nel vettore
    
    ard.close() # chiude la comunicazione seriale con Arduino
    
    avgddp=numpy.average(runningddp) # e lo analizza per trovare la media
    stdddp=numpy.std(runningddp) # e la deviazione standard

    print('Average and exp std:', avgddp, '+/-',stdddp) # le scrive sulla console
            
outputFile.close() # chiude il file dei dati 

print('end') # scrive sulla console che ha finito
