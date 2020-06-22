import paho.mqtt.client as mqtt
import threading
import json
from beacon import Beacon
from station import Station
from queue import Queue
from useful import string

q: "Queue[tuple]" = Queue()
beacons = set()
stations = list()


def worker():
    try:
        while True:
            msg = q.get()
            print(str(msg))

            station = Station.parse(msg[0])
            beacon = Beacon.parse(msg[1])
            station.add_beacon(beacon)

            stations.append(station)
            beacons.add(beacon.mac)

            print(f'Working on {msg}')
            print(f'Finished {msg}')
            q.task_done()
    except Exception:
        print('Exception -> worker')
    finally:
        q.task_done()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic/#")


def on_message(client, userdata, msg):
    print('Checkpoint')
    print(msg.topic + " " + str(msg.payload))
    # message = json.loads(str(msg.payload))
    message = json.loads(string)
    station = message['station']
    beacons_found = message['beacons']

    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    # send thirty task requests to the worker
    for beacon in beacons_found:
        q.put((station, beacon))
    print('All task requests sent\n', end='')

    # block until all tasks are done
    q.join()
    print('All work completed')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)  # "mqtt.eclipse.org"

client.loop_forever()
