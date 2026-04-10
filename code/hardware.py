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
const char* ssid = "iniya";
const char* password = "iniya123";

// ===== SERVER =====
const char* backendHost = "10.121.96.135";
const int backendPort = 5000;
String serverUrl;

// ===== ACCIDENT SETTINGS =====
float gForceThreshold = 0.5;     // accident threshold
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
  Serial.print("Connected to SSID: ");
  Serial.println(WiFi.SSID());
  Serial.print("BSSID: ");
  Serial.println(WiFi.BSSIDstr());

  serverUrl = String("http://") + backendHost + ":" + backendPort + "/data";
  Serial.print("Configured backend URL: ");
  Serial.println(serverUrl);
}

bool ipSameSubnet(const IPAddress &a, const IPAddress &b)
{
  return a[0] == b[0] && a[1] == b[1] && a[2] == b[2];
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

  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  Serial.print("Backend URL: ");
  Serial.println(serverUrl);

  // Quick connectivity check using raw WiFiClient
  WiFiClient testClient;
  if(!testClient.connect(backendHost, backendPort))
  {
    Serial.println("Network check failed: cannot connect to backend host on port 5000");
    Serial.print("ESP32 local IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("Backend host IP: ");
    Serial.println(backendHost);
    if(!ipSameSubnet(WiFi.localIP(), IPAddress(10, 121, 96, 135)))
    {
      Serial.println("⚠ Subnet mismatch: ESP32 and backend appear to be on different subnets.");
      Serial.println("  - Ensure ESP32 and PC are on the same Wi-Fi network.");
    }
    Serial.println("Firewall may be blocking port 5000 on the PC.");
    Serial.println("  - Allow port 5000 for Private networks in Windows Firewall.");
    return;
  }
  testClient.stop();

  HTTPClient http;

  bool started = http.begin(serverUrl);
  if(!started)
  {
    Serial.println("HTTP begin failed - check server URL and network");
    return;
  }

  http.addHeader("Content-Type","application/json");

  StaticJsonDocument<256> doc;

  doc["g_force"] = gForce;
  doc["lat"] = lat;
  doc["lon"] = lon;
  doc["gps_valid"] = gpsValid;
  doc["accident"] = accident;
  doc["hardware_id"] = "ESP32-01";

  String json;
  serializeJson(doc,json);

  const int maxRetries = 3;
  int attempt = 0;
  int httpResponseCode = -1;

  while(attempt < maxRetries)
  {
    attempt++;
    Serial.print("Attempt ");
    Serial.print(attempt);
    Serial.println("... POSTing data");

    httpResponseCode = http.POST(json);

    if(httpResponseCode > 0)
      break;

    Serial.print("POST failed (code ");
    Serial.print(httpResponseCode);
    Serial.println(") - retrying in 1s");
    delay(1000);
  }

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  if(httpResponseCode > 0)
  {
    String response = http.getString();
    Serial.print("Backend response: ");
    Serial.println(response);

    if(httpResponseCode >= 200 && httpResponseCode < 300)
    {
      Serial.println("Data posted successfully");
    }
    else
    {
      Serial.println("Warning: backend returned non-2xx status");
    }
  }
  else
  {
    Serial.print("Error sending data (HTTPClient final error): ");
    Serial.println(httpResponseCode);
    Serial.print("WiFi status: ");
    Serial.println(WiFi.status());
    if(WiFi.status() != WL_CONNECTED)
    {
      Serial.println("WiFi was disconnected during request.");
    }
    else
    {
      Serial.println("Check backend reachability and that port 5000 is open");
      Serial.print("Ping test from ESP to backend: ");
      if(WiFi.status() != WL_CONNECTED) Serial.println("skipped");
    }
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
