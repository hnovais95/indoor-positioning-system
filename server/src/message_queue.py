import ble_services
import paho.mqtt.client as mqtt
import utils
import threading
import positioning
import view
from location import Location
from random import randrange

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic/#")


def on_message(client, userdata, msg):
    # print(f'[on_message] {msg.topic} {str(msg.payload)}')
    payload_contents = utils.get_payload_contents(msg.payload)
    ble_services.refresh_devices(payload_contents)
    locations = positioning.run()
    #l = {'test': Location(randrange(5 + 1), randrange(5 + 1))}
    view.show(locations)    



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

t1 = threading.Timer(1.0, ble_services.show_devices)
#t1.start()

client.connect("localhost", 1883, 60)
try:
    client.loop_forever()
except Exception:
    client.loop_forever()