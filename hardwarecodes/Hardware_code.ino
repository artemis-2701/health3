

#define USE_ARDUINO_INTERRUPTS true 
#include <PulseSensorPlayground.h> // Includes the PulseSensorPlayground Library.
#include"DHT.h"
#define DHTPin 4  
#define DHTTYPE DHT11
DHT dht(DHTPin, DHTTYPE);
PulseSensorPlayground pulseSensor; 
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
const int PulseWire = 1; 
const int LED13 = 13; 
int Threshold = 100; 
 

#define REPORTING_PERIOD_MS 1000
 

 
// Connections : SCL PIN - D1 , SDA PIN - D2 , INT PIN - D0
PulseOximeter pox;
 
float BPM, SpO2;
uint32_t tsLastReport = 0;
 
 
void onBeatDetected()
{
    Serial.println("Beat Detected!");
}
float oxy= 94.5;



// DHT Sensor

               
       



#include <WiFi.h>
const char *ssid =  "Kurmanath's Wi-Fi Network";                                    // replace with your wifi ssid and wpa2 key
const char *password =  "Kurma@1969";
const char* server = "api.thingspeak.com";
WiFiClient client;


 String myWriteAPIKey = "BF4BHD99ZGN9HKSY";//"7PNU50AIBEZCXRRT";



// Variable to hold temperature readings
float num;
//uncomment if you want to get temperature in Fahrenheit
//float temperatureF;





void setup() {
   

  
//  WiFi.mode(WIFI_STA); 
  
  Serial.begin(9600);
  // Initialize ThingSpeak
  WiFi.begin(ssid, password);
 
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

  
   
  delay(500);//Delay to let system boot
  
  // Configure the PulseSensor object, by assigning our variables to it.
  pulseSensor.analogInput(PulseWire);
  pulseSensor.blinkOnPulse(LED13); //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);
  //Serial.println("DHT11 temperature A0");
  pinMode(34, INPUT); // ecg sensor
   dht.begin();
   delay(2000);
}

void loop() {
 
   
    //Start of Program 
//float  y=random(1, 401) / 100.0;
  float x=random(60, 70);
 // float x=0;
 
    float t=dht.readTemperature();
    Serial.print("temperature = ");
    Serial.print(t); 
    float ecg_sensor = (float(analogRead(34))-15; 
    Serial.println("C  ");
    delay(1000);
    int myBPM = pulseSensor.getBeatsPerMinute();
    Serial.print("BPM = ");
    Serial.println(myBPM); 
    delay(1000);
    float SpO2 = pox.getSpO2();
     Serial.print("SPO2 = ");
     Serial.println(sp02); 

    int field=7;
    float persp=3+random(50,200)/100;
    oxy=94+random(2,600)/100;
    if (client.connect(server,80))   //   "184.106.153.149" or api.thingspeak.com
    {  
                            
                             String postStr = myWriteAPIKey;
                             postStr +="&field3=";
                             postStr += String(t);
                             postStr +="&field4=";
                             postStr += String(myBPM);
                             postStr +="&field5=";
                             postStr += String(sp02);
                             postStr +="&field7=";
                             postStr += String(ecg_sensor);
                             postStr += "\r\n\r\n";
 
                             client.print("POST /update HTTP/1.1\n");
                             client.print("Host: api.thingspeak.com\n");
                             client.print("Connection: close\n");
                             client.print("X-THINGSPEAKAPIKEY: "+myWriteAPIKey+"\n");
                             client.print("Content-Type: application/x-www-form-urlencoded\n");
                             client.print("Content-Length: ");
                             client.print(String(postStr.length()));
                             client.print("\n\n");
                             client.print(postStr);
                             Serial.println("uploaded");
 
                             
     }
     delay(300);
          //client.stop();
   
    delay(20000);
 
  
}
