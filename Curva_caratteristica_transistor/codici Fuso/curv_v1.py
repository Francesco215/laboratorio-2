# Esperienza sulle curve caratteristiche del transistor. 
# Lo script scrive sulla porta seriale a cui e' collegato arduino un numero che viene interpretato da arduino come ritardo in unita' di 1 ms
# (fino a 9 ms) 
# Poi attende l'arrivo dei dati elaborati da arduino sulla seriale e li salva in un file
# Sulla console vengono scritte delle informazioni di rilievo (vedi dopo)

import serial # libreria per gestione porta seriale (USB)
import time   # libreria per temporizzazione

print('Apertura della porta seriale\n') # scrive sulla console (terminale)
ard=serial.Serial('/dev/ttyACM0',9600)  # apre la porta seriale /dev/ttyACM0
time.sleep(2)   # aspetta due secondi 

ard.write(b'1')#intervallo (ritardo) in unita' di ms <<<< questo si puo' cambiare (default messo a 1 ms, max 9 ms)
 
print('Start!\n') # scrive sulla console (terminale)
Directory='../dati_arduino/'   # nome directory dove salvare i file dati
FileName=(Directory+'peppa.txt') #nomina il file dati <<<< DA CAMBIARE SECONDO GUSTO 

outputFile = open(FileName, "w+" ) # apre file dati in scrittura


# loop lettura dati da seriale (sono 256 righe al massimo)
# nel loop viene controllata l'eventuale presenza della parola '9999' che indica la fine
# e nel caso il loop viene interrotto
nmis=0
runningV1max=0 # valore minimo iniziale della lettura di V1
runningV1min=1023 # valore massimo iniziale della lettura di V1
for i in range (0,256):        
    data = ard.readline().decode() # legge il dato e lo decodifica
    if (data == '9999\r\n'): break # interrompe la lettura quando incontra la fine del file (se meno di 256 punti)
    outputFile.write(data) # scrive i dati nel file
    runningV1=int(data[0:data.find(' ')]) # cerca il valore di V1, che e' dato dal primo intero scritto in data 
    if (runningV1>runningV1max):runningV1max=runningV1 # lo confronta con il massimo 
    if (runningV1<runningV1min):runningV1min=runningV1 # lo confronta con il minimo
    nmis+=1
         
outputFile.close() # chiude il file dei dati
ard.close() # chiude la comunicazione seriale con Arduino

print ('Number of data points acquired: ',nmis,'(out of 256)') # scrive sulla console quanti punti sono stati acquisiti
print ('V1 max: ',runningV1max,'   V1 min: ',runningV1min) # scrive il valore minimo e massimo di V1 (in digits)
print('end') # scrive sulla console che ha finito
