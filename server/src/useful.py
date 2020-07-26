def get_payload_contents(payload) -> str:
    aux = str(payload)
    return aux[2:(len(aux) - 1)]


def cloning(li1):
    li_copy = li1[:]
    return li_copy
