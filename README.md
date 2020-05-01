# Indoor Positioning System
Sistema de localização interna baseado em Bluetooth Low Energy

## ESP32
Os módulos ESP32 monitoram a presença de dispositivos BLE e reportam ao servior MQTT o MAC Adress e o RSSI dos respectivos dispositivos encontrados.

## Servidor MQTT
O broker Mosquitto recebe as informações das estações ES32 e as disponibiliza para os módulos externos realizarem a estimativa de posicionamento dos dispositivos BLE.

### TODO
* Implementar autodiagnóstico de estabilidade(tempuratura, frequência de perda das conexões e etc) nas estações ESP32
* Implementar watchdog contra travamento e instabilidade das estações ES32
* Implementar gerenciamento de energia com esp_sleep, visando autonomia das estações utilizando baterias
* Determinar algoritmo de estimativa de localização e implementar módulo
* Criar interface gráfica para visualização da localização no ambiente em tempo real
