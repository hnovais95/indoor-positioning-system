from station import Station
from beacon import Beacon


class Link:
    def __init__(self, station: Station, beacon_mac: str):
        self._station = station
        self._beacon_mac = beacon_mac

    @property
    def station(self) -> Station:
        return self._station

    @property
    def beacon_mac(self) -> str:
        return self._beacon_mac

    @property
    def distance(self) -> float:
        # y = A * x ^ B + C
        """a = 1.3173765600
        b = 7.0280800100
        c = -0.6409702466

        beacon: Beacon = self._station.beacons_found[self._beacon_mac]

        if (beacon.rssi is None):
            return -1.0

        ratio = beacon.rssi * 1.0 / beacon.tx_power

        if (ratio < 1.0):
            return ratio ** 10
        else:
            return a * ratio ** b + c"""
        beacon: Beacon = self._station.beacons_found[self._beacon_mac]
        measured_power = -55
        n = 2
        return 10**((measured_power - beacon.rssi) / (10**n))

    def __str__(self):
        return f'Link:\n\tStation: {self._station.mac}\n\tBeacon: {self._beacon_mac}\n\tDistance: {self.distance}'
