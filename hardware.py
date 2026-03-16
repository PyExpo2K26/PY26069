#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

const char* ssid = "YOUR_HOTSPOT_NAME";
const char* password = "YOUR_PASSWORD";
const char* serverUrl = "http://192.168.X.X:5000/data"; // Use 'ipconfig' to get this

void setup() {
  Serial.begin(115200);
  if(!accel.begin()){ Serial.println("No ADXL345 found"); while(1); }
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
}

void loop() {
  sensors_event_t event; 
  accel.getEvent(&event);
  
  // Calculate total G-force magnitude
  float g_total = sqrt(pow(event.acceleration.x,2) + pow(event.acceleration.y,2) + pow(event.acceleration.z,2)) / 9.8;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    String httpRequestData = "{\"g_force\":" + String(g_total) + "}";
    int httpResponseCode = http.POST(httpRequestData);
    
    Serial.print("G-Force: "); Serial.println(g_total);
    http.end();
  }
  delay(500);
}