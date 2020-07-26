from station import Station
from typing import Set, Dict
import paho.mqtt.client as mqtt
import useful
import json

beacons: Set[str] = set()
stations: Dict[str, Station] = dict()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic/#")


def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    payload_contents = useful.get_payload_contents(msg.payload)
    refresh(payload_contents)


def refresh(payload: str):
    message = json.loads(payload)
    station = Station.parse(message)
    stations[station.mac] = station

    for beacon_mac in station.beacons_found:
        beacons.add(beacon_mac)

    for beacon_mac in beacons:
        beacon_found = False
        for station in stations.values():
            if beacon_mac in station.beacons_found:
                beacon_found = True
                break

        if beacon_found is False:
            beacons.remove(beacon_mac)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
