# from message_queue import stations, beacons
from typing import Dict
from test import beacons, stations
import numpy as np

beacon_distances: Dict[str, list] = dict()
locations: Dict[str, tuple] = dict()


def trilateration():
    for beacon_mac in beacons:
        # list with stations linked to the beacon and their respective
        # three best distances
        # list[tuple[station_mac, distances]]
        distances = get_shorter_distances(beacon_mac)
        d = []
        x = []
        y = []
        for i in range(len(distances)):
            mac = distances[i][0]
            d.append(distances[i][1])
            x.append(stations[mac].location[0])
            y.append(stations[mac].location[1])

        A = np.array([[2*(x[0] - x[2]), 2*(y[0] - y[2])],
                      [(2*x[1] - x[2]), 2*(y[1] - y[2])]])

        b = np.array(
            [x[0] ** 2 - x[2] ** 2 + y[0] ** 2 + d[2] ** 2 - d[0] ** 2,
             x[1] ** 2 - x[2] ** 2 + y[1] ** 2 + d[2] ** 2 - d[1] ** 2])

        locations[beacon_mac] = np.linalg.solve(A, b)

    print(f'Locations: {locations}')


def calculate_distances():
    for beacon_mac in beacons:
        # search beacon at stations
        for station_mac, station in stations.items():
            if beacon_mac in station.beacons_found:
                distance = station.calculate_distance(beacon_mac)
                beacon_distances.setdefault(beacon_mac, []).append(
                    (station_mac, distance))


def get_shorter_distances(beacon_mac: str):
    better_distances = list()
    rank_distances(beacon_mac)
    for index, item in enumerate(beacon_distances[beacon_mac]):
        if index == 3:
            break
        station = item[0]
        distance = item[1]
        better_distances.append((station, distance))
    return better_distances


def rank_distances(beacon_mac: str):
    beacon_distances[beacon_mac] = sorted(
        beacon_distances[beacon_mac], key=lambda k: k[1])


def print_distances():
    for k, v in beacon_distances.items():
        print(f'Beacon MAC: [{k}]\n\
Linked Stations(station_mac, distances): {v}\n')


""" Test
if __name__ == '__main__':
    calculate_distances()
    print_distances()
    trilateration()"""
