from ble import BLE
from datetime import datetime


class Beacon(BLE):
    def __init__(self, name: str, mac: str, manufecturer: str,
                 rssi: int = None, tx_power: int = None):
        super().__init__(name, mac, manufecturer, rssi, tx_power)
        self._timestamp = datetime.now()

    @staticmethod
    def parse(input: dict = None):
        if input is None:
            raise NotImplementedError()

        beacon_attributes = list(vars(BLE).keys()) + \
            list(vars(Beacon).keys())
        input_attributes = vars(input).keys()

        is_beacon = True
        for atrribute in input_attributes:
            if atrribute[1:] not in beacon_attributes:
                is_beacon = False
                break

        if is_beacon:
            return Beacon(input['name'], input['mac'],
                          input['manufecturer'], input['rssi'],
                          input['tx_power'])
        else:
            return None

    @property
    def timestamp(self):
        return self._timestamp
