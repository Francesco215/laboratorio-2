# Esperienza sulla curva caratteristica del diodo. 
# Lo script scrive sulla porta seriale a cui e' collegato arduino un numero che viene interpretato da arduino come ritardo in unita' di 10 ms 
# Poi attende l'arrivo dei dati elaborati da arduino sulla seriale e li salva in un file

import serial # libreria per gestione porta seriale (USB)
import time   # libreria per temporizzazione

print('Apertura della porta seriale\n') # scrive sulla console (terminale)
ard=serial.Serial('/dev/ttyACM0',9600)  # apre la porta seriale /dev/ttyACM0
time.sleep(2)   # aspetta due secondi 

ard.write(b'5')#intervallo (ritardo) in unita' di 10 ms <<<< questo si puo' cambiare (default messo a 50 ms)
 
print('Start!\n') # scrive sulla console (terminale)
Directory='../dati_arduino/'   # nome directory dove salvare i file dati
FileName=(Directory+'diodo.txt') # nomina il file dati <<<< DA CAMBIARE SECONDO GUSTO 

outputFile = open(FileName, "w+" ) # apre file dati in scrittura


# loop lettura dati da seriale (sono 256 righe, eventualmente da aggiustare)
for i in range (0,256):
    data = ard.readline().decode() # legge il dato e lo decodifica
    if data:
            outputFile.write(data) # scrive i dati nel file
            
outputFile.close() # chiude il file dei dati

ard.close() # chiude la comunicazione seriale con Arduino

print('end') # scrive sulla console (terminale)
