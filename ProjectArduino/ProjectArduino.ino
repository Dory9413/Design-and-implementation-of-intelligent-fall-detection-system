#include <Adafruit_Sensor.h> 
#include <Adafruit_ADXL345_U.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

#define WIRE1 Wire
#define PIN_WIRE1_SDA        (70u)
#define PIN_WIRE1_SCL        (71u)

#define STATE_NORMAL 0
#define STATE_CRITICAL_QUESTION 1
#define STATE_CRITICAL 2

#define CRITICAL_ASK_TIME_RANGE_SECONDS 30

#define HEART_RATE_SIZE 20
#define ACC_ROLLING_WINDOW_SIZE 40

#define PIN_ACCEPT 2
#define PIN_REJECT 3

float a;
float b;
float c;

float X[ACC_ROLLING_WINDOW_SIZE];
float Y[ACC_ROLLING_WINDOW_SIZE];
float Z[ACC_ROLLING_WINDOW_SIZE];

int loopCounter;

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified();  

MAX30105 particleSensor;
byte rates[HEART_RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute;
int beatAvg;
String gps_data = "";
String gps_lat = "";
String gps_long = "";
String server_response = "";

int state = STATE_NORMAL;
int startCriticalTime;

void send_sms() {
  String number = "+989204102757";
  if (gps_data = "no fix"){
    gps_lat = "35.747057";
    gps_long = "51.461595";
  }
  String text = "Location: https://maps.google.com?q=" + gps_lat + "," + gps_long + "\nHeartRate: " + String(beatAvg);
  Serial.println("send sms");
  Serial.flush();
  Serial2.print("AT+CMGS=\"" + number + "\"\r\n");
  delay(1000);
  Serial2.print(text);
  delay(1000);
  Serial2.write(0x1a);
  for (int i = 0; i < 20; i++) {
    Serial.print(".");
    Serial.flush();
    delay(1000);
  }  
}


void updateHeartRate() {
  Serial.flush();
  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue) == true) {
    //We sensed a beat!
    long delta = millis() - lastBeat;
    lastBeat = millis();

    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
      rateSpot %= HEART_RATE_SIZE; //Wrap variable

      //Take average of readings
      beatAvg = 0;
      for (byte x = 0 ; x < HEART_RATE_SIZE ; x++)
        beatAvg += rates[x];
      beatAvg /= HEART_RATE_SIZE;
    }
  }
  Serial.println("Updated heartrate");
  Serial.flush();
  if (irValue < 50000){
    Serial.print("No finger?");
    beatAvg = -1;
  }
}


void updateLocation() {
  Serial.println("Updating location");
  Serial.flush();
  gps_data = "";
  if (Serial2.available() > 0) 
    Serial2.readString();
  Serial2.print("AT+CGNSINF\r\n");
  Serial2.flush(); 
  while (Serial2.available() == 0 ) {} 
  gps_data = Serial2.readString(); 
  delay(1000);
  if (gps_data.charAt(gps_data.indexOf(",") + 1) == '1') {
    gps_data = gps_data.substring(gps_data.indexOf(",") + 1);
    gps_data = gps_data.substring(gps_data.indexOf(",") + 1);
    gps_data = gps_data.substring(gps_data.indexOf(",") + 1);
    gps_lat = gps_data.substring(0, gps_data.indexOf(",") - 1);
    gps_data = gps_data.substring(gps_data.indexOf(",") + 1);
    gps_long = gps_data.substring(0, gps_data.indexOf(",") - 1);
    gps_data = "";
    gps_data = gps_long + "," + gps_lat; 
  }
  else {
    gps_data = "no fix";
  }
  Serial.flush();
  Serial.println(gps_data);
  Serial.flush();
  Serial.println("Updated location");
  Serial.flush();
  
}

void updateAccel() {
  Serial.println("Updating accel");
  Serial.flush();
  sensors_event_t event; 
  accel.getEvent(&event);

  a = event.acceleration.x;
  b = event.acceleration.y;
  c = (event.acceleration.z) - 9.803;
  
  for(int i = 0; i < ACC_ROLLING_WINDOW_SIZE - 1; i++) {
    X[i] = X[i+1];
    Y[i] = Y[i+1];
    Z[i] = Z[i+1];
  }
  X[ACC_ROLLING_WINDOW_SIZE-1] = a;
  Y[ACC_ROLLING_WINDOW_SIZE-1] = b;
  Z[ACC_ROLLING_WINDOW_SIZE-1] = c;
  
  Serial.println("Updated accel");
  Serial.flush();
}

void check_connect() {
  char ccalr[]={"+CCALR: 1"};
  Serial.println("WAITING TO CONNECT TO NETWORK");
  Serial.flush();
  while (true) {
    Serial2.print("AT+CCALR?\r\n");
    if (Serial2.find(ccalr) == true) 
      break;
  }
  Serial.println("CONNECTED TO NETWORK");
  Serial.flush();
}


String send_data(String host, String path, String post_data) {
  check_connect();
  char closeok[] = {"CLOSE OK"};
  char connectok[]={"CONNECT OK"};
  uint32_t tm = 0;
  //CONNECT OK
  if (Serial2.available() > 0)
    Serial2.readString();
  tm = millis();
  Serial2.print("AT+CIPSTART=\"TCP\",\"" + host + "\",8001\r\n");
  Serial2.flush();
  while (Serial2.find(connectok) == false) {   
    if ((millis() - tm) >  30000) {
      Serial2.print("AT+CFUN=1,1\r\n");
      delay(1000);
      check_connect();
      return "ERR-Connection error";
    }
  }
  Serial.println("SUCCESSFULLY CONNECTED");
  Serial.flush();
  
  String data = "POST " + path + " HTTP/1.1\r\nHost: " + host +":8001 "+"\r\nContent-Type: application/json\r\nContent-Length: " + String(post_data.length()) + "\r\n\r\n" + post_data + "\r\n\r\n";
  String command = "AT+CIPSEND=";
  command = command + String(data.length());
  command = command + "\r\n";
  Serial2.print(command);
  delay(100);
  server_response = "";
  Serial2.flush();
  if (Serial2.available() > 0)
  {
    Serial2.readString();
  }  
  tm = millis();
  Serial2.print(data);
  Serial2.flush();
  while ((millis() - tm ) < 7000) {
    if (Serial2.available() > 0) {
      server_response.concat(char(Serial2.read()));
      Serial.println("reading server's response...");
    }
  }
  if (Serial2.available() > 0)
    Serial2.readString();


  tm = millis();  
  Serial2.print("AT+CIPCLOSE\r\n");
  Serial2.flush();  
  while (Serial2.find(closeok) == false && ((millis() - tm) < 5000 )) {}
  Serial.println("server response:");
  Serial.println(server_response);
  Serial.flush();
  return "ok";
}

void initCritical() {
  Serial.println("*** CRITICAL ***");
  state = STATE_CRITICAL;
  send_sms();
  state = STATE_NORMAL;
}

void acceptCritical() {
  if(state == STATE_CRITICAL_QUESTION) {
    initCritical();
  }
}

void rejectCritical() {
  if(state == STATE_CRITICAL_QUESTION || state == STATE_CRITICAL) {
    Serial.println("cancel sms");
    state = STATE_NORMAL;
  }
}

void setup() {
  Serial2.begin(9600);
  Serial.begin(9600);
  check_connect();
  if(!accel.begin())
   {
      Serial.println("No valid sensor found");
      while(1);
   }
  Serial2.print("ATE0\r\n");
  delay(1000);
  Serial2.print("AT+CGNSPWR=1\r\n");
  delay(2000);
  
  state = STATE_NORMAL;
  loopCounter = 0;

  pinMode(PIN_ACCEPT, INPUT);
  pinMode(PIN_REJECT, INPUT); 

  if (!particleSensor.begin(Wire1, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);
  for(int i=0; i<2000; i++){
    updateHeartRate();
    Serial.println(beatAvg);
  }
  Serial.println("Setup OK.");
}

void loop() {
  loopCounter++;
  updateAccel();
  Serial.print("State is: ");
  Serial.println(state);
  
  switch(state) {
    case STATE_NORMAL:
      {
        //TODO check server response if crit go to STATE_CRITICAL_QUESTION, set  and break
        //startCriticalTime = millis();
        if(loopCounter % 40 != 0) {
          break;
        }
        Serial.println("creating data");
        //TODO get GPS, acc and heartrate
        //TODO send gps acc heartrate to server - event 0
        for(int i=0; i<2000; i++){
          updateHeartRate();
          Serial.println(beatAvg);
        }
        updateLocation();
        String jsonData = "{\"event\":0,\"acc\":[";
        for(int i = 0; i < ACC_ROLLING_WINDOW_SIZE; i++) {
          jsonData += "[";
          jsonData += String(X[i],2);
          jsonData += ",";
          jsonData += String(Y[i],2);
          jsonData += ",";
          jsonData += String(Z[i],2);
          jsonData += "]";
          if(i != ACC_ROLLING_WINDOW_SIZE - 1) {
            jsonData += ",";
          }
        }
        jsonData += "],";
        jsonData += "\"heartRate\":";
        jsonData += String(beatAvg);
        jsonData += ",";
        jsonData += "\"gpsData\":\"";
        jsonData += gps_data;
        jsonData += "\"";
        jsonData += "}";
        Serial.println(jsonData);
        
        send_data("188.121.120.164", "/users/app/save-acc-data/", jsonData);
        Serial.println(server_response);
        bool isFall = false;
        int statusCode = server_response.indexOf("HTTP/1.1 200");
        Serial.println("Found 200 status at: " + String(statusCode));
        Serial.println(server_response.substring(statusCode, statusCode+10));
        if(statusCode != -1) {
          isFall = true;
          Serial.println("Fall detected!");
        } else {
          isFall = false;
          Serial.println("Normal data (Not Fall)");
        }
        if (isFall) {
          startCriticalTime = millis();
          state = STATE_CRITICAL_QUESTION;
        }
        break;
      }
    case STATE_CRITICAL_QUESTION:
      { 
        digitalRead(PIN_ACCEPT);
        digitalRead(PIN_REJECT);
        if(digitalRead(PIN_ACCEPT) == HIGH)
          acceptCritical();
        else if(digitalRead(PIN_REJECT) == HIGH)
          rejectCritical();
        if(millis() - startCriticalTime > CRITICAL_ASK_TIME_RANGE_SECONDS*1000) {
          initCritical();
          break;
        }
        break;
      }
    case STATE_CRITICAL:
      {
        //TODO get GPS, acc and heartrate
        //TODO send gps acc heartrate to server - event 1
        break;
      }
  }

}
