from typing import Optional
from ble import BLE
from beacon import Beacon


class Station(BLE):
    def __init__(self, name: str, mac: str, manufecturer: str):
        super().__init__(name, mac, manufecturer)
        self._beacons_found: dict = {}
        self._location = None

    @staticmethod
    def parse(msg: dict = None):
        if msg is None:
            raise NotImplementedError()

        station_attributes = list(vars(BLE).keys()) + \
            list(vars(Station).keys())
        msg_attributes = msg.keys()

        is_station = True
        for atrribute in msg_attributes:
            if atrribute not in station_attributes:
                is_station = False
                break

        if is_station:
            st = Station(msg['name'], msg['mac'],
                         msg['manufecturer'])

            for item in msg['beacons_found']:
                st.add_beacon(Beacon(
                    item['name'], item['mac'], item['manufecturer'],
                    item['rssi'], item['tx_power']))

            return st
        else:
            return None

    def add_beacon(self, beacon: Beacon):
        self._beacons_found[beacon.mac] = beacon

    @property
    def beacons_found(self):
        return self._beacons_found

    @property
    def location(self) -> Optional[tuple]:
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def calculate_distance(self, beacon_mac: str) -> float:
        # y = A * x ^ B + C
        a = 1.3173765600
        b = 7.0280800100
        c = -0.6409702466

        beacon = self.beacons_found[beacon_mac]

        if (beacon.rssi is None):
            return -1.0

        ratio = beacon.rssi * 1.0 / beacon.tx_power

        if (ratio < 1.0):
            return ratio ** 10
        else:
            return a * ratio ** b + c
