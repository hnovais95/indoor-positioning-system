from ble import BLE
from datetime import datetime


class Beacon(BLE):
    def __init__(self, name: str, mac: str, manufacturer: str,
                 rssi: int = None, tx_power: int = None):
        super().__init__(name, mac, manufacturer, rssi, tx_power)
        self._timestamp = datetime.now()

    @staticmethod
    def parse(msg: dict = None):
        if msg is None:
            raise NotImplementedError()

        beacon_attributes = list(vars(BLE).keys()) + \
            list(vars(Beacon).keys())
        msg_attributes = vars(msg).keys()

        is_beacon = True
        for atrribute in msg_attributes:
            if atrribute[1:] not in beacon_attributes:
                is_beacon = False
                break

        if is_beacon:
            return Beacon(msg['name'], msg['mac'],
                          msg['manufacturer'], msg['rssi'],
                          msg['tx_power'])
        else:
            return None

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return f'Beacon: {self._name} MAC: {self._mac} Manufecturer: {self._manufacturer}'
