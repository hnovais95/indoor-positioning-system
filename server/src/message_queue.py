import common
import paho.mqtt.client as mqtt
import useful
import threading
import positioning


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic/#")


def on_message(client, userdata, msg):
    # print(f'[on_message] {msg.topic} {str(msg.payload)}')
    payload_contents = useful.get_payload_contents(msg.payload)
    common.refresh_devices(payload_contents)
    positioning.run()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

t1 = threading.Timer(1.0, common.show_devices)
t1.start()

client.connect("localhost", 1883, 60)
client.loop_forever()
