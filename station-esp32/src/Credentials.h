/**
 * @file Credentials.h
 * @brief Credentials for connecting to the server
 * @copyright Heitor Novais
*/

#ifndef CREDENTIALS_H_
#define CREDENTIALS_H_

/*******************************************************************
*   CONSTANTS
*******************************************************************/
/**
 * WiFi credentials
*/
const char *ssid = "Heitor";
const char *password = "amazonas";

/**
 * MQTT credentials
*/
const char *mqttServer = "192.168.0.12";
const uint16_t mqttPort = 1883;
const char *mqttClient = "ESP32-1";
const char *mqttTopico = "test/topic/#";

#endif