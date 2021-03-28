from link import Link
from typing import List


def get_payload_contents(payload) -> str:
    aux = str(payload)
    return aux[2:(len(aux) - 1)]


def cloning(li1) -> list:
    li_copy = li1[:]
    return li_copy


def sort_links(links: List[Link]) -> List[Link]:
    return sorted(links, key=lambda k: k.distance)
