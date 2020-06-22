def get_payload_contents(payload) -> str:
    aux = str(payload)
    return aux[2:(len(aux) - 1)]
