from station import Station
from beacon import Beacon
from typing import Optional

class Link:
    def __init__(self, station: Station, beacon_mac: str):
        self._station = station
        self._beacon = self._station.beacons_found[beacon_mac]

    @property
    def station(self) -> Station:
        return self._station

    @property
    def beacon(self) -> str:
        return self._beacon

    @property
    def distance(self) -> Optional[float]:
        measured_power = -60
        n = 2
        return 10**((measured_power - self._beacon.rssi) / (10*n))

    def __str__(self):
        #return f'\n\tStation: {self._station.mac}\n\tBeacon: {self._beacon.name}\n\tDistance: {self.distance}'
        return f'{self._beacon.rssi};{round(self.distance, 2)}'
