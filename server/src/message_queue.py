import paho.mqtt.client as mqtt
import json
from station import Station
import useful

beacons = set()
stations = dict()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic/#")


def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    payload_contents = useful.get_payload_contents(msg.payload)

    message = json.loads(payload_contents)
    st = Station.parse(message)
    stations[st.mac] = st

    for beacon_mac in st.beacons_found:
        beacons.add(beacon_mac)

    print(f'Stations: {stations}')
    print(f'Beacons: {beacons}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
