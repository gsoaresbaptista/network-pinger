from packet import get_timestamp


def create_packet(
    packet_id: str,
    packet_type: str,
    message: str,
    time: str | None = None,
) -> bytes:
    '''Generate a standard-compliant packet
    In order, the packet consists of:
        - 5 bytes, sequence number
        - 1 byte, ping = 0 or pong = 1
        - 4 bytes, timestamp
        - 30 bytes, packet content
    :param packet_id - int, sequence number
    :param packet_type - int, 0 to ping and 1 to pong
    :param message - str, packet content
    :return packet - bytes, packet as byte stream
    '''
    id_str = packet_id.rjust(5, '0')
    ping_std = packet_type  # 0 = ping, 1 = pong
    timestamp = get_timestamp() if time is None else time
    packet_message = id_str + ping_std + timestamp + message.ljust(30, '\0')
    return packet_message.encode('ascii')
