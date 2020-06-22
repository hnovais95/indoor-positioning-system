from ble import BLE
from beacon import Beacon


class Station(BLE):
    def __init__(self, name: str, mac: str, manufecturer: str):
        super().__init__(name, mac, manufecturer)
        self._beacons_found: dict = {}

    @staticmethod
    def parse(args: dict = None):
        if args is None:
            raise NotImplementedError()
        station_attributes = vars(Station).keys()
        dict_attributes = vars(args).keys()

        is_station = True
        for atrribute in dict_attributes:
            if atrribute[1:] not in station_attributes:
                is_station = False
                break

        if is_station:
            return Station(args['nome'], args['mac'],
                           args['manufecturer'])
        else:
            return None

    def add_beacon(self, beacon: Beacon):
        self._beacons_found[beacon.mac] = beacon

    @property
    def beacons_found(self):
        return self._beacons_found

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
