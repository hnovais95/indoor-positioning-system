/**
 * @file main.cpp
 * @brief Beacon Station ESP32
 * @warning
 * @todo esp sleep; diagnostic tool (connections, temperature and so on); watchdogs
 * @bug
 * @copyright Heitor Novais
*/

#include <Arduino.h>
#include <vector>
#include <sstream>
#include <string>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include "Connectivity.h"

/*******************************************************************
*   DEFINES
*******************************************************************/
#define SCAN_TIME 5

/*******************************************************************
*   TYPEDEFS
*******************************************************************/
/**
 * Struct with MAC Address and RSSI of beacon finded
*/ 
typedef struct {
  char address[17];  // ex.: 67:f1:d2:04:cd:5d
  int rssi = 0;
} BeaconData;

/*******************************************************************
*   GLOBAL VARIABLES
*******************************************************************/
std::vector<BeaconData> buffer;
char *mqttTopico = "teste/ble";

/*******************************************************************
*   CLASSES
*******************************************************************/
class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
  public:    
    void onResult(BLEAdvertisedDevice advertisedDevice)
    {
        extern std::vector<BeaconData> buffer;
        BeaconData beacon;
        
        if (advertisedDevice.haveRSSI()) {
          beacon.rssi = advertisedDevice.getRSSI();
          strcpy(beacon.address, advertisedDevice.getAddress().toString().c_str());
        }

        buffer.push_back(beacon);

        // Print everything via serial port for debugging
        Serial.printf("MAC: %s \n", advertisedDevice.getAddress().toString().c_str());
        Serial.printf("name: %s \n", advertisedDevice.getName().c_str());
        Serial.printf("RSSI: %d \n\n", advertisedDevice.getRSSI());
    }
};

/*******************************************************************
*   LOCAL PROTOTYPES
*******************************************************************/
void scanBeacons();
/**
 * Mount JSON message 
*/ 
String mountMessage();

/*******************************************************************
*   IMPLEMENTATION
*******************************************************************/
void setup()
{
  Serial.begin(115200);
  connectWiFi();
  connectMQTT();
  BLEDevice::init("");
}

void loop()
{
  Serial.println("Devices found:");
  scanBeacons();
  
  checkConnections();

  client.loop();

  String message = mountMessage();

  bool result = client.publish(mqttTopico, message.c_str(), true);
  Serial.print("PUB Result: ");
  Serial.println(result);
  Serial.println("--\n");

  buffer.clear();
}

/*******************************************************************
*   FUNCTIONS
*******************************************************************/
void scanBeacons()
{
  BLEScan *pBLEScan = BLEDevice::getScan(); //create new scan
  MyAdvertisedDeviceCallbacks cb;
  pBLEScan->setAdvertisedDeviceCallbacks(&cb);
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster

  BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME);

  // Stop BLE
  pBLEScan->stop();
  Serial.println("Scan done!");
  Serial.println();
}

/**
 * Mount JSON message 
*/ 
String mountMessage()
{
  String json = "\n[\n";
  for (uint8_t i = 0; i < buffer.size(); i++)
  {
    BeaconData beacon = buffer.at(i);
    
    json += "  {\n";
    json += "    \"MAC\": ";
    json += String(beacon.address);
    json += ",\n";
    json += "    \"RSSI\": ";    
    json += String(beacon.rssi);
    json += "\n  }";

    if (i < buffer.size() - 1)
      json += ",\n";
  }
  json += "\n]";  
  
  Serial.print("Message:");
  Serial.println(json);
  Serial.println();

  return json;
}