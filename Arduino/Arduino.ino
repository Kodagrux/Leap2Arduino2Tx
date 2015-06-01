#include <SimpleTimer.h>
#define PPM_PIN 2
#define THRUST_PIN A0

#define ERROR_PIN 11
#define STATUS_PIN 12
#define TX_PIN 13

boolean thurstControl = false;

SimpleTimer timer;

char inData[100];
String inString = "";
int index = 0;
int nrOfCh = 0;
boolean stringComplete = false;

int Fixed_uS = 300;       // PPM frame fixed LOW phase
int pulseMin = 650;       // pulse minimum width minus start in uS

int chData[8];

// a function to be executed periodically
void ppmoutput() {
  for (int i = 0; i < nrOfCh; i++) {
    digitalWrite(PPM_PIN, LOW);
    delayMicroseconds(Fixed_uS);    // Hold
    digitalWrite(PPM_PIN, HIGH);
    delayMicroseconds(chData[i] + pulseMin);  //Channels
  }
  
  // Synchro pulse
  digitalWrite(PPM_PIN, LOW);
  delayMicroseconds(Fixed_uS);    // Hold
  digitalWrite(PPM_PIN, HIGH);  // Start Synchro pulse
}

void setup() {
  nrOfCh = 8;
  Serial.begin(9600);
  
  pinMode(ERROR_PIN, OUTPUT);
  pinMode(STATUS_PIN, OUTPUT);
  pinMode(TX_PIN, OUTPUT);
  
  startUp();
  
  timer.setInterval(22, ppmoutput);
  pinMode(PPM_PIN, OUTPUT);
  
  
  for (int i = 0; i < nrOfCh; i++) {
    chData[i] = 550 + i * 30;
  }
}

void loop() {
  timer.run();
  //Serial.println(nrOfCh);
  if (stringComplete) {
    ParseSerialData();  
    inString = "";    
    stringComplete = false; 
    digitalWrite(TX_PIN, LOW);
  }
  
  if (thurstControl) {
    chData[2] = map(analogRead(THRUST_PIN), 0, 1023, 113, 937);
  } /*else {
    
  }*/
}


void ParseSerialData() {
  char *p = inData;
  char *str;   
  int count = 0;
  while ((str = strtok_r(p, ",", &p)) != NULL) {
    if (count == 2 && atoi(str) == -1) {
      digitalWrite(STATUS_PIN, HIGH);
      thurstControl = true;
      chData[count] = map(analogRead(THRUST_PIN), 0, 1023, 113, 937);
    } else {
      chData[count] = atoi(str);
    }
    count++;      
  }
}


void serialEvent() {
  while (Serial.available() && stringComplete == false) {
    digitalWrite(TX_PIN, HIGH);
    char inChar = Serial.read(); 
    inData[index] = inChar; 
    index++;     
    inString += inChar;
    if (inChar == '\n') {
      
      index = 0;
      stringComplete = true;
    }
  }
}

void startUp() {
  for(int i = 0; i < 3; i++) {
    digitalWrite(ERROR_PIN, LOW);
    digitalWrite(STATUS_PIN, LOW);
    digitalWrite(TX_PIN, LOW);
    delay(100);
    digitalWrite(ERROR_PIN, HIGH);
    digitalWrite(STATUS_PIN, HIGH);
    digitalWrite(TX_PIN, HIGH);
    delay(100);
  }
  delay(700);
  digitalWrite(ERROR_PIN, LOW);
  delay(100);
  digitalWrite(STATUS_PIN, LOW);
  delay(100);
  digitalWrite(TX_PIN, LOW);
  delay(300);
  
  if (analogRead(THRUST_PIN) > 2) {
    digitalWrite(ERROR_PIN, HIGH);
  } else {
    digitalWrite(STATUS_PIN, HIGH); 
  }
}
