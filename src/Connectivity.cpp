/**
 * @file Connectivity.cpp
 * @brief Connects ESP32 station to server
 * @copyright Heitor Novais
*/

#include <Arduino.h>
#include "Connectivity.h"
#include "Credentials.h"

/*******************************************************************
*   GLOBAL VARIABLES
*******************************************************************/
WiFiClient esp32;
PubSubClient client(esp32);

/*******************************************************************
*   BODY FUNCTIONS
*******************************************************************/
void connectWiFi()
{
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());  
  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());
}

void connectMQTT()
{
  client.setServer(mqttServer, mqttPort);
  Serial.println("Connecting to MQTT...");
  if (client.connect(mqttClient))
  {
    Serial.println("Connected!");
  }
  else
  {
    Serial.print("failed with state ");
    Serial.println(client.state());
    delay(2000);
  }
}

/**
 * Attempts to reconnect if disconnected
*/
void checkConnections()
{
  while (WiFi.status() != WL_CONNECTED)
  {
    connectWiFi();
  }

  while (!client.connected())
  {
    connectMQTT();
  }
}