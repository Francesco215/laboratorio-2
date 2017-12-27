/* 
Questo sketch serve per acquisire forme d'onda dipendenti dal tempo in modalita'
glued. Vengono eseguite in successione 4 acquisizioni con un ritardo variabile
rispetto al trigger. La porta analogica letta è A0 e il trigger digitale e' sulla porta 5.
In ogni acquisizione vengono acquisiti 256 punti. Il files complessivo avra'
256x4=1024 righe e due colonne (rispettivamente t in us e valore digitalizzato).
*/

// Blocco definizioni
const unsigned int analogPin=0; // Definisice la porta A0 per la lettura
const unsigned int sincPin = 5;  //pin 5 ingresso digitale per la sincronizzazione con il generatore
int i; // Definisice la variabile intera i (contatore)
int delays; // Definisce la variabile intera delays
int V[256]; // Definisce l'array intero V
long t[256]; // Definisce l'array t
unsigned long StartTime; // Definisce il valore StartTime
unsigned long delayus; // Definisce variabile per acquisizione multipla
unsigned long delayms; // Definisce variabile ausiliaria tempo totale acq
int start=0; // Definisce il valore start (usato come flag)
int sinc; // Variabile di sincronizzazione
int j; // Variabile di loop multiacquisizione

// Istruzioni di inizializzazione
void setup()
  {
   Serial.begin(19200); // Inizializza la porta seriale a 19200 baud
   Serial.flush(); // Pulisce il buffer della porta seriale 
   pinMode(sincPin, INPUT);  //pin sincPin configurato come ingresso digitale
   //analogReference(INTERNAL); // Sceglie il riferimento V_ref = 1.1 V (nominali)
   bitClear(ADCSRA,ADPS0); // Istruzioni necessarie per velocizzare
   bitClear(ADCSRA,ADPS2); // il rate di acquisizione analogica
  }

// Istruzioni del programma
void loop()
  {
    delayus=0; // Valori iniziali variabili di ritardo
    delayms=0;
    
    if (Serial.available() >0) // Controlla se il buffer seriale ha qualcosa
      {
        delays = (Serial.read()-'0')*100; // Legge il byte e lo interpreta come ritardo
        Serial.flush(); // Svuota la seriale
	start=1; // Pone il flag start a uno
      }
 
  if(!start) return // Se il flag e' start=0 non esegue le operazioni qui di seguito
                    // altrimenti le fa partire (quindi aspetta di ricevere l'istruzione
                    // di partenza    
    delay(1000); // Aspetta 1000 ms per evitare casini
    for (j=0;j<8;j++)
     {
 //   delay(1000); // Aspetta 1000 ms per evitare casini
    sinc = digitalRead(sincPin);//legge sincPin
    while (sinc==HIGH) // ciclo di attesa iniziale per sincronizzazione, attende che sincPin vada basso
      {sinc = digitalRead(sincPin);} //legge sincPin
    while (sinc==LOW) // ciclo di attesa iniziale per sincronizzazione, attende che sincPin vada alto
      {sinc = digitalRead(sincPin);}//legge sincPin    
     StartTime=micros(); // Misura il tempo iniziale con l'orologio interno
    if (j==0)
      {
      for(i=0;i<2;i++) // Loop di due misure a vuoto (da fare solo all'inizio)
        {
        V[i]=analogRead(analogPin);
        }
       }
       if (j>0)
       {
       delayMicroseconds(delayus+delays);
       delay(delayms);
       }
    for(i=0;i<256;i++) // Loop di misura 
      {
          t[i]=micros()-StartTime; // Legge il timestamp e lo mette in array t
          V[i]=analogRead(analogPin); // Legge analogPin e lo mette in array V
          delayMicroseconds(delays); // Aspetta tot us
      }
    delayms=floor(t[255]/1000);
    delayus=t[255]-delayms*1000;
    for(i=0;i<256;i++) // Loop per la scrittura su porta seriale
      {
        Serial.print(t[i]); // Scrive t[i]
        Serial.print(" "); // Mette uno spazio
        Serial.println(V[i]); // Scrive V[i] e va a capo
      }
       delay(1000); // Aspetta 1000 ms per evitare casini
   }

    start=0; // Annulla il flag
    Serial.flush(); // Pulisce il buffer della porta seriale (si sa mai)
}

