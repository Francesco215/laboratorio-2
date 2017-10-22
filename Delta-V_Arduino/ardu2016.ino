/* 
Questo sketch serve per acquisire 256 coppie di dati (tempo in us, d.d.p. in unita' di 
digitalizzazione) attraverso Arduino;
la tensione viene campionata sull'ingresso analogico A0; 
l'intervallo temporale di campionamento nominale e' aggiustabile in unita'  
di 100 us (da 100 a 900 us) tramite carattere scritto nello script di Python;
la porta 7 viene usata come uscita e mantenuta a livello alto
*/

// Blocco definizioni
const unsigned int analogPin=0; // Definisice la porta A0 per la lettura
const int digitalPin_uno=7; // Definisce la porta 7 usata come output ref
int i; // Definisice la variabile intera i (contatore)
int delays; // Definisce la variabile intera delays
int V[256]; // Definisce l'array intero V
long t[256]; // Definisice l'array t
unsigned long StartTime; // Definisce il valore StartTime
int start=0; // Definisce il valore start (usato come flag)

// Istruzioni di inizializzazione
void setup()
  {
   Serial.begin(19200); // Inizializza la porta seriale a 19200 baud
   Serial.flush(); // Pulisce il buffer della porta seriale 
   digitalWrite(digitalPin_uno,HIGH); // Pone digitalPin_uno a livello alto
   //analogReference(INTERNAL); // Sceglie il riferimento V_ref = 1.1 V (nominali)
   bitClear(ADCSRA,ADPS0); // Istruzioni necessarie per velocizzare
   bitClear(ADCSRA,ADPS2); // il rate di acquisizione analogica
  }

// Istruzioni del programma
void loop()
  {
    if (Serial.available() >0) // Controlla se il buffer seriale ha qualcosa
      {
        delays = (Serial.read()-'0')*100; // Legge il byte e lo interpreta come ritardo
        Serial.flush(); // Svuota la seriale
	start=1; // Pone il flag start a uno
      }
 
  if(!start) return // Se il flag e' start=0 non esegue le operazioni qui di seguito
                    // altrimenti le fa partire (quindi aspetta di ricevere l'istruzione
                    // di partenza
    delay(2000); // Aspetta 2000 ms per evitare casini 

     for(i=0;i<2;i++) // Fa un ciclo di due letture a vuoto per "scaricare" l'analogPin
       {
        V[i]=analogRead(analogPin);
       }
    StartTime=micros(); // Misura il tempo iniziale con l'orologio interno
    for(i=0;i<256;i++) // Loop di misura 
      {
          t[i]=micros()-StartTime; // Legge il timestamp e lo mette in array t
          V[i]=analogRead(analogPin); // Legge analogPin e lo mette in array V
          delayMicroseconds(delays); // Aspetta tot us
      }
  
    for(i=0;i<256;i++) // Loop per la scrittura su porta seriale
      {
        Serial.print(t[i]); // Scrive t[i]
        Serial.print(" "); // Mette uno spazio
        Serial.println(V[i]); // Scrive V[i] e va a capo
      }
  
    start=0; // Annulla il flag
    Serial.flush(); // Pulsice il buffer della porta seriale (si sa mai)
}

