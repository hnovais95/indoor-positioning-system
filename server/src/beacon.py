from ble import BLE


class Beacon(BLE):
    def __init__(self, name: str, mac: str, manufecturer: str,
                 rssi: int = 0, tx_power: int = 0):
        super().__init__(name, mac, manufecturer, rssi,)

    @staticmethod
    def parse(args: dict = None):
        if args is None:
            raise NotImplementedError()
        beacon_attributes = vars(Beacon).keys()
        dict_attributes = vars(args).keys()

        is_beacon = True
        for atrribute in dict_attributes:
            if atrribute[1:] not in beacon_attributes:
                is_beacon = False
                break

        if is_beacon:
            return Beacon(args['nome'], args['mac'],
                          args['manufecturer'], args['rssi'],
                          args['tx_power'])
        else:
            return None
