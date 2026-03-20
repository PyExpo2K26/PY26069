#include <Wire.h>
#include <TinyGPS++.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <math.h>

#define ADXL345_ADDR 0x53
#define BUZZER 25
#define LED 26

TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

// ===== WIFI =====
const char* ssid = "ESP";
const char* password = "nihil1017";

// ===== SERVER =====
const char* serverUrl = "http://10.121.234.29:5000/data";

// ===== ACCIDENT SETTINGS =====
float gForceThreshold = 1.0;     // accident threshold
int accidentConfirmCount = 0;
const int requiredConfirmations = 1;

// Accelerometer values
float ax, ay, az;

void setup()
{
  Serial.begin(115200);

  Wire.begin(21,22);

  pinMode(BUZZER, OUTPUT);
  pinMode(LED, OUTPUT);

  gpsSerial.begin(9600, SERIAL_8N1, 16, 17);

  // ===== Start ADXL345 =====
  Wire.beginTransmission(ADXL345_ADDR);
  Wire.write(0x2D);
  Wire.write(0x08);
  Wire.endTransmission();

  Wire.beginTransmission(ADXL345_ADDR);
  Wire.write(0x31);
  Wire.write(0x08);
  Wire.endTransmission();

  // ===== WIFI CONNECT =====
  WiFi.begin(ssid,password);

  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

// =========================
// READ ACCELEROMETER
// =========================

void readADXL345()
{
  Wire.beginTransmission(ADXL345_ADDR);
  Wire.write(0x32);
  Wire.endTransmission(true);

  Wire.requestFrom(ADXL345_ADDR,6);

  if(Wire.available()==6)
  {
    int16_t x = Wire.read() | Wire.read()<<8;
    int16_t y = Wire.read() | Wire.read()<<8;
    int16_t z = Wire.read() | Wire.read()<<8;

    ax = x * 0.0039;
    ay = y * 0.0039;
    az = z * 0.0039;
  }
}

// =========================
// SEND DATA TO BACKEND
// =========================

void sendAccidentData(float gForce,float lat,float lon,bool gpsValid,bool accident)
{
  if(WiFi.status()!=WL_CONNECTED)
  {
    Serial.println("WiFi not connected");
    return;
  }

  HTTPClient http;

  http.begin(serverUrl);

  http.addHeader("Content-Type","application/json");

  StaticJsonDocument<200> doc;

  doc["g_force"] = gForce;
  doc["lat"] = lat;
  doc["lon"] = lon;
  doc["gps_valid"] = gpsValid;
  doc["accident"] = accident;

  String json;

  serializeJson(doc,json);

  Serial.println("Sending JSON:");
  Serial.println(json);

  int httpResponseCode = http.POST(json);

  if(httpResponseCode > 0)
  {
    Serial.print("HTTP Response: ");
    Serial.println(httpResponseCode);

    String response = http.getString();
    Serial.println(response);
  }
  else
  {
    Serial.print("Error sending data: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

// =========================
// MAIN LOOP
// =========================

void loop()
{

  // Read GPS data
  while(gpsSerial.available()>0)
  {
    gps.encode(gpsSerial.read());
  }

  // Read accelerometer
  readADXL345();

  float magnitude = sqrt(ax*ax + ay*ay + az*az);

  Serial.print("Magnitude: ");
  Serial.println(magnitude);

  // Accident detection
  if(magnitude > gForceThreshold)
  {
    accidentConfirmCount++;
    Serial.print("Accident count: ");
    Serial.println(accidentConfirmCount);

    if(accidentConfirmCount >= requiredConfirmations)
    {
      digitalWrite(BUZZER,HIGH);
      digitalWrite(LED,HIGH);

      Serial.println("🚨 ACCIDENT DETECTED");

      float lat = 0;
      float lon = 0;

      bool gpsValid = gps.location.isValid();

      if(gpsValid)
      {
        lat = gps.location.lat();
        lon = gps.location.lng();

        Serial.print("Latitude: ");
        Serial.println(lat,6);

        Serial.print("Longitude: ");
        Serial.println(lon,6);
      }
      else
      {
        Serial.println("⚠ GPS not valid – sending 0,0");
      }

      sendAccidentData(magnitude,lat,lon,gpsValid,true);

      delay(10000);

      accidentConfirmCount = 0;
    }
  }

  else
  {
    accidentConfirmCount = 0;

    digitalWrite(BUZZER,LOW);
    digitalWrite(LED,LOW);
  }

  delay(2000);
}