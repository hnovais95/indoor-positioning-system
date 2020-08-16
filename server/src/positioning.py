from common import on_site_beacons, on_site_stations
from location import Location
from link import Link
from typing import Optional, List, Dict
import numpy as np
import useful


def trilateration() -> Optional[Dict[str, Location]]:
    locations: Dict[str, Location] = dict()
    links: List[Link] = establish_links()

    for beacon_mac in on_site_beacons:
        beacon_links = get_beacon_links(links, beacon_mac)

        if len(beacon_links) > 2:
            shorter_links: List[Link] = get_shorter_links(beacon_links)
            d = []
            x = []
            y = []

            for link in shorter_links:
                station = link.station
                d.append(link.distance)
                x.append(station.location.x)
                y.append(station.location.y)

            A = np.array([[2*(x[0] - x[2]), 2*(y[0] - y[2])],
                          [(2*x[1] - x[2]), 2*(y[1] - y[2])]])

            b = np.array(
                [x[0] ** 2 - x[2] ** 2 + y[0] ** 2 + d[2] ** 2 - d[0] ** 2,
                    x[1] ** 2 - x[2] ** 2 + y[1] ** 2 + d[2] ** 2 - d[1] ** 2])

            result = np.linalg.solve(A, b)
            location = Location(result[0], result[1])
            print(f'[trilateration] Location: ({location.x}, {location.y}')
            locations[beacon_mac] = location
        else:
            print('[trilateration] Number of links must be greater than 3.')
    return locations


def establish_links() -> List[Link]:
    links: List[Link] = list()
    for beacon_mac in on_site_beacons:
        for station in on_site_stations.values():
            if beacon_mac in station.beacons_found:
                link = Link(station, beacon_mac)
                links.append(link)
    return links


def get_beacon_links(links: List[Link], beacon_mac: str) -> List[Link]:
    beacon_links: List[Link] = list()
    for link in links:
        if link.beacon_mac == beacon_mac:
            beacon_links.append(link)
    return beacon_links


# get the best three distances
def get_shorter_links(beacon_links: List[Link]) -> List[Link]:
    sorted_links = useful.sort_links(beacon_links)
    better_links: List[Link] = list()
    for i in np.arange(3):
        better_links.append(sorted_links[i])
    return better_links


def run():
    trilateration()
