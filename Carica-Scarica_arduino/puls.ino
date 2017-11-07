/* 
Questo sketch serve per accendere e spegnere periodicamente e
indefinitamente la porta digitale 7 di Arduino. La porta è accesa 
per i tempi in ms indicati in delayON e spenta per i tempi in ms
indicati in delayOFF. Il periodo e' quindi T = delayON + delayOFF
*/

// Blocco dichiarazioni
const int digitalPin_uno=7; // Definisce la porta 7 usata per la carica
const int ledPin = 13; // Definisce la porta 13 collegata al led
const int digitalPin_due=5;
const int delayON = 50; // Definisce la durata di accensione
const int delayOFF = 100; // Definisce la durata di spegnimento

// Istruzioni di inizializzazione
void setup()
  {
   pinMode(digitalPin_uno,OUTPUT); // Definisce digitalPin_uno come output
   pinMode(ledPin,OUTPUT); // Definisce ledPin come output
   digitalWrite(digitalPin_uno,LOW); // Pone digitalPin_uno a livello bass
   digitalWrite(digitalPin_due,LOW);
   digitalWrite(ledPin,LOW); // Pone ledPin a livello basso
  }

// Istruzioni del programma
void loop()
  {
    delay(delayOFF);
    digitalWrite(digitalPin_due,HIGH);
    delayMicroseconds(100);
    digitalWrite(digitalPin_due,LOW);
    digitalWrite(digitalPin_uno,HIGH);
    digitalWrite(ledPin,HIGH);
    delay(delayON);
    digitalWrite(digitalPin_due,HIGH);
    delayMicroseconds(100);
    digitalWrite(digitalPin_due,LOW);
    digitalWrite(digitalPin_uno,LOW);
    digitalWrite(ledPin,LOW);
  }
