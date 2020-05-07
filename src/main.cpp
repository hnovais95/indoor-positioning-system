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
#include <BLEBeacon.h>
#include "Connectivity.h"

/*******************************************************************
*   DEFINES
*******************************************************************/
#define SCAN_TIME 5
#define BEACON_UUID "16bffbc8-8ff8-11ea-bc55-0242ac130003"
#define MQTT_TOPIC "teste/ble"

/*******************************************************************
*   TYPEDEFS
*******************************************************************/
/**
 * @brief Struct with MAC Address and RSSI of finded beacon
 * 
 */ 
typedef struct {
  char address[17];  // ex.: 67:f1:d2:04:cd:5d
  int rssi = 0;
} BeaconData;

/*******************************************************************
*   GLOBAL VARIABLES
*******************************************************************/
/**
 * @brief Buffer of finded beacons
 * 
 */ 
std::vector<BeaconData> buffer;
/**
 * @brief Advertising object
 * 
 */ 
BLEAdvertising *pAdvertising;

/*******************************************************************
*   CLASSES
*******************************************************************/
/**
 * @brief Define callback class
 * 
 */
class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
  public:
    /**
     * @brief Callback function
     * 
     */
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
        Serial.printf("Name: %s \n", advertisedDevice.getName().c_str());
        Serial.printf("MAC: %s \n", advertisedDevice.getAddress().toString().c_str());
        Serial.printf("RSSI: %d \n\n", advertisedDevice.getRSSI());
    }
};

/*******************************************************************
*   LOCAL PROTOTYPES
*******************************************************************/
/**
 * @brief Configure advertising
 * 
 */
void setBeacon();
/**
 * @brief Start advertising
 * 
 */
void startAdvertising();
/**
 * @brief Discover beacons
 * 
 */
void scanBeacons();
/**
 * @brief Mount JSON message
 * 
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
  startAdvertising();
}

void loop()
{
  Serial.println("Devices found:");
  scanBeacons();
  
  checkConnections();

  client.loop();

  String message = mountMessage();

  bool result = client.publish(MQTT_TOPIC, message.c_str(), true);
  Serial.print("PUB Result: ");
  Serial.println(result ? "Success!" : "Failed!");
  Serial.println("--\n");

  buffer.clear();
}

/*******************************************************************
*   FUNCTIONS
*******************************************************************/
/**
 * @brief Configure advertising
 * 
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
  oAdvertisementData.setName("ESP32-01");
  
  std::string strServiceData = "";
  
  strServiceData += (char)26;     // Len
  strServiceData += (char)0xFF;   // Type
  strServiceData += oBeacon.getData(); 
  oAdvertisementData.addData(strServiceData);
  
  pAdvertising->setAdvertisementData(oAdvertisementData);
  pAdvertising->setScanResponseData(oScanResponseData);
}
/**
 * @brief Start advertising
 * 
 */
void startAdvertising()
{
  pAdvertising = BLEDevice::getAdvertising();
  setBeacon();   
  pAdvertising->start(); // Start advertising
  Serial.println("Advertizing started...");
}
/**
 * @brief Discover beacons
 * 
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
  //Serial.println("Scan done!");
  //Serial.println();
}
/**
 * @brief Mount JSON message 
 * @todo Minify message
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
  
  //Serial.print("Message:");
  //Serial.println(json);
  //Serial.println();

  return json;
}