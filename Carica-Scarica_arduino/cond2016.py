import serial # libreria per gestione porta seriale (USB)
import time # libreria per temporizzazione
import numpy

nacqs = 1 # numero di acquisizioni da registrare (ognuna da 256x2 coppie di punti)

FileName='pippo'  # parte comune nome file << DA CAMBIARE SECONDO NECESSITA'
Directory = '../dati_arduino/' # directory dei files di dati
FileNameC=(Directory+FileName+'_C.txt') # crea nome file dati carica
FileNameS=(Directory+FileName+'_S.txt') # crea nome file dati scarica
outputFileC = open(FileNameC, "w" ) # apre file dati predisposto per scrittura carica
outputFileS = open(FileNameS, "w" ) # apre file dati predisposto per scrittura scarica

print('Please wait')

for j in range (1,nacqs+1):    
    ard=serial.Serial('/dev/ttyACM0',19200)  # apre porta seriale (occhio alla sintassi)
    print('Start Acquisition ',j, ' of ',nacqs) # scrive sulla console (terminale)
    time.sleep(2)   # aspetta due secondi per evitare casini
    
    ard.write(b'1') # scrive il carattere per l'intervallo di campionamento
                    # in unita' di 100 us << DA CAMBIARE A SECONDA DEI GUSTI
                    # l'istruzione b indica che e' un byte (carattere ASCII)   
    time.sleep(2) # aspetta due secondi per evitare casini  
    # loop lettura dati carica da seriale (256 coppie di dati: tempo in us, valore digitalizzato di d.d.p.)    
    for i in range (0,256):
        data = ard.readline().decode() # legge il dato e lo decodifica
        if data:
            outputFileC.write(data) # scrive i dati sul file
    # loop lettura dati scarica da seriale (256 coppie di dati: tempo in us, valore digitalizzato di d.d.p.) 
    for i in range (0,256):
        data = ard.readline().decode() # legge il dato e lo decodifica
        if data:
            outputFileS.write(data) # scrive i dati sul file    
    ard.close() # chiude la comunicazione seriale con Arduino            
outputFileC.close() # chiude il file dei dati per la carica
outputFileS.close() # chiude il file dei dati per la scarica
print('end') # scrive sulla console che ha finito
