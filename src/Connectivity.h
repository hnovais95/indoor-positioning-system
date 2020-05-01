#ifndef CONNECTIVITY_H_
#define CONNECTIVITY_H_

#include <WiFi.h>
#include <PubSubClient.h>

extern WiFiClient esp32;
extern PubSubClient client;


void connectWiFi();

void connectMQTT();

void checkConnections();

#endif