#include <SimpleTimer.h>
#define PPM_PIN 2

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
  }
}


void ParseSerialData() {
  char *p = inData;
  char *str;   
  int count = 0;
  while ((str = strtok_r(p, ",", &p)) != NULL) {  
    chData[count] = atoi(str);
    count++;      
  }
}


void serialEvent() {
  while (Serial.available() && stringComplete == false) {
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
