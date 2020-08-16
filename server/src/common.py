from typing import Set, Dict
from station import Station
import threading
import json

on_site_beacons: Set[str] = set()
on_site_stations: Dict[str, Station] = dict()


def refresh_devices(payload: str):
    message = json.loads(payload)
    station = Station.parse(message)
    on_site_stations[station.mac] = station

    for beacon_mac in station.beacons_found:
        on_site_beacons.add(beacon_mac)

    for beacon_mac in on_site_beacons:
        beacon_found = False
        for station in on_site_stations.values():
            if beacon_mac in station.beacons_found:
                beacon_found = True
                break

        if beacon_found is False:
            on_site_beacons.remove(beacon_mac)


def show_devices():
    for station in on_site_stations.values():
        print(f'[show_devices]  Station: {str(station)}')
        print("\t\tBeacons found:")
        for beacon in station.beacons_found.values():
            print(f'\t\t\t{str(beacon)}')
    t2 = threading.Timer(3.0, show_devices)
    t2.start()
