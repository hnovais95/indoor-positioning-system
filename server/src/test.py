from beacon import Beacon
from station import Station
import random

stations = dict()
beacons = set()

for i in range(1, 5):
    st = Station('station' + str(i), '0x0' + str(i), 'heitor')
    st.location = (random.randint(0, 30), random.randint(0, 30))
    stations[st.mac] = st

for i in range(1, 17):
    beacon = None
    if i % 3 == 0:
        beacon = Beacon('beacon' + str(i), '0x0' + str(3), 'heitor',
                        random.randint(-30, 0), random.randint(-30, 0))
        beacons.add(beacon.mac)
    elif i % 2 == 0:
        beacon = Beacon('beacon' + str(i), '0x0' + str(2), 'heitor',
                        random.randint(-30, 0), random.randint(-30, 0))
        beacons.add(beacon.mac)
    else:
        beacon = Beacon('beacon' + str(i), '0x0' + str(1), 'heitor',
                        random.randint(-30, 0), random.randint(-30, 0))
        beacons.add(beacon.mac)

    for station in stations.values():
        if beacon.mac not in station.beacons_found:
            station.add_beacon(beacon)
            break
