/*
Programma per la misura della curva caratteristica di collettore del transistor.
Il transistor viene alimentato da un'onda triangolare prodotta dal generatore di funzioni.
L'onda triangolare deve essere opportunamente configurata (ampiezza tra 0 e 5 V e periodo opportuno).
L'uscita TTL/CMOS del generatore va collegata al pin 5 di Arduino configurato come ingresso digitale
per consentire la sincronizzazione (partenza loop di lettura con inizio salita onda triangolare)
Nel loop di acquisizione vengono effettuate due letture utilizzando gli ingressi analogici A0 e A2.    
Il pin A0 digitalizza la tensione letta in uscita dal generatore (indirettamente fornisce una misura della corrente che passa nel diodo).
Il pin A2 digitalizza la tensione VCE.
*/

const unsigned int sincPin = 5;  //pin 5 ingresso digitale per la sincronizzazione con il generatore
const unsigned int digitalPin = 7; //pin 7 uscita digitale (serve per eventuale calibrazione convertitore)
const unsigned int analogPin_uno=0;  //pin A0 per lettura V1
const unsigned int analogPin_due=2;  //pin A2 per lettura V2
unsigned int i=0;  //variabile di conteggio per i cicli
int V1[256];  //array per memorizzare V1 (d.d.p, letta da analogPin_uno) 
int V2[256];  //array per memorizzare V2 (d.d.p, letta da analogPin_due)
int delayms;  //variabile che contiene il ritardo tra due step successivi (in unita' di 1 ms, fino a 9 ms)
int start=0;  //flag per dare inizio alla misura 
int sinc; //variabile di sincronizzazione
int nmis=0; //variabile con il numero di punti acquisiti

//Inizializzazione
void setup()
{
  pinMode(sincPin, INPUT);  //pin sincPin configurato come ingresso digitale
  Serial.begin(9600);  //inizializzazione della porta seriale
  Serial.flush(); // svuota il buffer della porta seriale 
}

//Ciclo di istruzioni del programma
void loop()
{
    if (Serial.available() >0) // Controlla se il buffer seriale ha qualcosa
      {
        delayms = (Serial.read()-'0')*1; // Legge il byte e lo interpreta come ritardo (unita' 1 ms)
        Serial.flush(); // Svuota il buffer della seriale
	start=1; // Pone il flag start a uno
      } 
  if(!start) return // solo se il flag e' a uno parte l'acquisizione
    delay(2000); // attende 2s per evitare casini
    digitalWrite(digitalPin,HIGH); // pone digitalPin a livello alto (per eventuale calibrazione)
    sinc = digitalRead(sincPin);//legge sincPin
    while (sinc==LOW) // ciclo di attesa iniziale per sincronizzazione, attende che sincPin vada alto
      {sinc = digitalRead(sincPin);} //legge sincPin
    while (sinc==HIGH) // ciclo di attesa iniziale per sincronizzazione, attende che sincPin vada basso
      {sinc = digitalRead(sincPin);}//legge sincPin
      for(i=0;i<256;i++)  //ciclo di acquisizione temporizzata delle misure (fino a 256 punti)
        {
         sinc = digitalRead(sincPin); //legge sincPin
         if (sinc==HIGH) break; //esce dal ciclo se sincPin torna alto
         delay(delayms);   //aspetta il tempo impostato
         V1[i]=analogRead(analogPin_uno);   //legge il pin analogPin_uno
         V2[i]=analogRead(analogPin_due);   //legge il pin analogPin_due
       }
     nmis = i;  //scrive in nmis il numero effettivo di punti acquisiti
     for(i=0;i<nmis;i++)  //nuovo ciclo che scorre gli array di dati e li scrive sulla seriale 
     {
       Serial.print(V1[i]);  
       Serial.print(" ");
       Serial.println(V2[i]);
     }
     if (nmis<256) //se il numero di punti è minore di 256 scrive un carattere convenzionale di fine file
       {
         Serial.println(9999);  //il carattere convenzionale è 9999
       }
    start=0; // Annulla il flag
    Serial.flush(); // svuota il buffer della porta seriale
  }

