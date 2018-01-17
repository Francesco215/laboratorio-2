/*
Programma per la misura della caratteristica I-V del diodo.
Si utilizza un'uscita digitale PWM (pin 5) variando il duty cycle dell'onda quadra da 0% al 100% (o altro valore) lentamente. 
L'onda quadra viene inviata in ingresso ad un integratore RC per ottenere una tensione continua via via crescente, cioè una rampa a scalini. Lo step è regolabile in unità di 10 ms e ad ogni step vengono effettuate due letture utilizzando gli ingressi analogici A0 e A2.    
Il pin A0 digitalizza la tensione letta in uscita dal filtro (indirettamente fornisce una misura della corrente che passa nel diodo)
Il pin A2 digitalizza la tensione ai capi del diodo.
*/

const unsigned int RampPin = 5;  //pin 5 uscita pwm per generare la rampa. Questo pin viene collegato all'integratore 
const unsigned int analogPin_uno=0;  //pin A0 per lettura V1
const unsigned int analogPin_due=2;  //pin A2 per lettura V2
unsigned int i=0;  //variabile che conta gli step durante la salita della rampa
int V1[256];  //array per memorizzare V1 (d.d.p, letta da analogPin_uno) 
int V2[256];  //array per memorizzare V2 (d.d.p, letta da analogPin_due)
int delay_ms;  //variabile che contiene il ritardo tra due step successivi (in unita' di 10 ms)
int start=0;  //flag per dare inizio alla misura 

//Inizializzazione
void setup()
{
  pinMode(RampPin, OUTPUT);  //pin pwm RampPin configurato come uscita  
  Serial.begin(9600);  //inizializzazione della porta seriale
  Serial.flush(); // svuota il buffer della porta seriale
}

//Ciclo di istruzioni del programma
void loop()
{
    if (Serial.available() >0) // Controlla se il buffer seriale ha qualcosa
      {
        delay_ms = (Serial.read()-'0')*10; // Legge il byte e lo interpreta come ritardo (unita' 10 ms)
        Serial.flush(); // Svuota il buffer della seriale
	start=1; // Pone il flag start a uno
      } 
  if(!start) return // solo se il flag è a uno parte l'acquisizione
    delay(500); // attende 0.5s per evitare casini
    if (start==1)  
      analogWrite(RampPin,0); // all'inizio pone a 0 la RampPin per favorire scarica condensatore
    delay(1500); // attende 1.5s per scaricare condensatore 
    for(i=0;i<256;i++)  //il valore che definisce il duty cycle dell'onda quadra è scrivibile su 8 bit
                         //cioè assume valori da 0-->duty cycle 0%(uscita sempre in stato LOW) a 256-->duty cycle 100% (livello costante HIGH)
      {
       analogWrite(RampPin, i); //incrementa il duty cycle di uno step
       delay(delay_ms);   //aspetta il tempo impostato
       V1[i]=analogRead(analogPin_uno);   //legge il pin analogPin_uno
       V2[i]=analogRead(analogPin_due);   //legge il pin analogPin_due
       delay(delay_ms);   //aspetta il tempo impostato
      }
     for(i=0;i<256;i++)  //nuovo ciclo che scorre gli array di dati e li scrive sulla seriale 
     {
       Serial.print(V1[i]);  
       Serial.print(" ");
       Serial.println(V2[i]);
     }
    start=0; // Annulla il flag
    Serial.flush(); // svuota il buffer della porta seriale
  }



