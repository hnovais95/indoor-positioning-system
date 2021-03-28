/**
   @file main.cpp
   @brief Beacon Station ESP32
   @warning
   @todo esp sleep; diagnostic tool (connections, temperature and so on); watchdogs
   @bug
   @copyright Heitor Novais
*/
#include <Arduino.h>
#include <vector>
#include <sstream>
#include <string>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEBeacon.h>
#include "Connectivity.h"
#include <PubSubClient.h>
/*******************************************************************
    DEFINES
*******************************************************************/
#define SCAN_TIME 1
#define BEACON_UUID "16bffbc8-8ff8-11ea-bc55-0242ac130002"
/*******************************************************************
    TYPEDEFS
*******************************************************************/
/**
   @brief Struct with Location by station

*/
typedef struct {
  float x = 0.0;
  float y = 0.0;  
} Location;
/**
   @brief Struct with MAC Address and RSSI of finded beacon

*/
typedef struct {
  char name[20];
  char address[17];  // ex.: 67:f1:d2:04:cd:5d
  int rssi = 0;
  int txPower = 0;
  char manufacturer[20];
} BeaconData;
/*******************************************************************
    GLOBAL VARIABLES
*******************************************************************/
/**
   @brief Buffer of finded beacons

*/
std::vector<BeaconData> buffer;
/**
   @brief Advertising object

*/
BLEAdvertising *pAdvertising;
/**
   @brief Station location objetct

*/
Location location;
/**
   @brief Station name
*/
const char* stationName = "station1";
/**
   @brief Advertising appearance name
*/
const char* appearanceName = "ESP32-01";
/*******************************************************************
    CLASSES
*******************************************************************/
/**
   @brief Define callback class

*/
class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
  public:
    /**
       @brief Callback function

    */
    void onResult(BLEAdvertisedDevice advertisedDevice)
    {
      extern std::vector<BeaconData> buffer;
      BeaconData beacon;

      if (advertisedDevice.haveRSSI())
      {
        beacon.rssi = advertisedDevice.getRSSI();
        strcpy(beacon.address, advertisedDevice.getAddress().toString().c_str());
      } 
      else
        return;

      if (advertisedDevice.haveName())
        strcpy(beacon.name, advertisedDevice.getName().c_str());

      if (advertisedDevice.haveTXPower())
        beacon.txPower = advertisedDevice.getTXPower();

      //if (advertisedDevice.haveManufacturerData())
        //strcpy(beacon.manufacturer, advertisedDevice.getManufacturerData().c_str());

      buffer.push_back(beacon);

      // Print everything via serial port for debugging
      Serial.printf("Name: %s \n", advertisedDevice.getName().c_str());
      //Serial.printf("MAC: %s \n", advertisedDevice.getAddress().toString().c_str());
      Serial.printf("RSSI: %d \n", advertisedDevice.getRSSI());
      //Serial.printf("TXPower: %d \n", advertisedDevice.getTXPower());
      //Serial.printf("ManufacturerData: %s \n", advertisedDevice.getManufacturerData());
    }
};
/*******************************************************************
    LOCAL PROTOTYPES
*******************************************************************/
/**
   @brief Set station location

*/
void setLocation();
/**
   @brief Configure advertising

*/
void setBeacon();
/**
   @brief Start advertising

*/
void startAdvertising();
/**
   @brief Discover beacons

*/
void scanBeacons();
/**
   @brief Mount JSON message

*/
String mountMessage();
/**
   @brief Validade beacon

*/
bool validadeBeacon(BeaconData beacon);
/*******************************************************************
    IMPLEMENTATION
*******************************************************************/
void setup()
{
  Serial.begin(115200);
  setLocation(0.0, 10.0);
  connectWiFi();
  connectMQTT();
  BLEDevice::init("");
  startAdvertising();
}

void loop()
{
  Serial.println("Devices found:");
  scanBeacons();
  checkConnections();
  client.loop();
  String message = mountMessage();
  bool result = client.publish("test/topic", message.c_str(), true);
  Serial.print("PUB Result: ");
  Serial.println(result ? "Success!" : "Failed!");
  Serial.println("--\n");
  buffer.clear();
}
/*******************************************************************
    FUNCTIONS
*******************************************************************/
/**
   @brief Set station location

*/
void setLocation(float x, float y)
{
  location.x = x;
  location.y = y;
}
/**
   @brief Configure advertising

*/
void setBeacon()
{
  BLEBeacon oBeacon = BLEBeacon();
  oBeacon.setManufacturerId(0x4C00); // fake Apple 0x004C LSB (ENDIAN_CHANGE_U16!)
  oBeacon.setProximityUUID(BLEUUID(BEACON_UUID));
  oBeacon.setMajor((1 & 0xFFFF0000) >> 16);
  oBeacon.setMinor(1 & 0xFFFF);
  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
  BLEAdvertisementData oScanResponseData = BLEAdvertisementData();

  oAdvertisementData.setFlags(0x04); // BR_EDR_NOT_SUPPORTED 0x04
  oAdvertisementData.setName(appearanceName);

  std::string strServiceData = "";

  strServiceData += (char)26;     // Len
  strServiceData += (char)0xFF;   // Type
  strServiceData += oBeacon.getData();
  oAdvertisementData.addData(strServiceData);

  pAdvertising->setAdvertisementData(oAdvertisementData);
  pAdvertising->setScanResponseData(oScanResponseData);
}
/**
   @brief Start advertising

*/
void startAdvertising()
{
  pAdvertising = BLEDevice::getAdvertising();
  setBeacon();
  pAdvertising->start(); // Start advertising
  Serial.println("Advertizing started...");
}
/**
   @brief Discover beacons

*/
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
   @brief Mount JSON message
   @todo Minify message
*/
String mountMessage()
{
  /*
   * Ex.:
     {\"name\":\"station1\",\"mac\":\"aa:bb:cc:dd:aa\",\"manufecturer\":\"espressif\",\"location\":{\"x\":0,\"y\":0},\"beacons_found\":[{\"name\":\"beacon1\",\"mac\":\"aa:bb:cc:dd:ee\",\"manufecturer\":\"espressif\",\"rssi\":-20,\"tx_power\":-30},{\"name\":\"beacon2\",\"mac\":\"aa:bb:cc:dd:ff\",\"manufecturer\":\"espressif\",\"rssi\":-30,\"tx_power\":-30}]}"
  */
  String json = "{\"name\":\"" + String(stationName) + "\",\"mac\":\"" + String(WiFi.macAddress()) + "\",\"manufacturer\":\"" + "espressif" + "\",\"location\":{\"x\":" + String(location.x) + ",\"y\":" + String(location.y) + "},\"beacons_found\":["; 
  for (uint8_t i = 0; i < buffer.size(); i++)
  {
    BeaconData beacon = buffer.at(i);
    if (validadeBeacon(beacon))
    {
      json += "{";
      json += "\"name\":\"";
      json += String(beacon.name) + "\",";
      json += "\"mac\":\"";
      json += String(beacon.address) + "\",";
      json += "\"manufacturer\":\"";
      json += String("samsung") + "\",";//"\",";//String(beacon.manufacturer) + "\",";
      json += "\"rssi\":";
      json += String(beacon.rssi) + ",";
      json += "\"tx_power\":";
      json += String(beacon.txPower);
      json += "}";
      if (i < buffer.size() - 1)
        json += ",";
    }
  }
  json += "]}";
  Serial.print("Message:");
  Serial.println(json);
  Serial.println();

  return json;
}

bool validadeBeacon(BeaconData beacon)
{
  if (sizeof(beacon.name) == 0) return false;
  if (sizeof(beacon.address) == 0) return false;
  if (sizeof(beacon.manufacturer) == 0) return false;
  if (beacon.rssi > 0) return false;
  return true;
}

/*
 typedef struct {
  char name[20];
  char address[17];  // ex.: 67:f1:d2:04:cd:5d
  int rssi = 0;
  int txPower = 0;
  char manufacturer[20];
} BeaconData;
 */
