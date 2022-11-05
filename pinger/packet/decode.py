from typing import Tuple


def read_packet(packet: str) -> Tuple[str, str, str, str]:
    '''Handle a standard-compliant packet
    Unpack all packet data into single variables
    :param packet - str, packet decoded in ascii format
    :return
        - id_sequence - int, sequence number
        - packet_type - int, 0 if ping or 1 for pong
        - timestamp - int, timestamp in seconds
        - content - str, packet content
    '''
    id_sequence = packet[:5]
    packet_type = packet[5]
    timestamp = packet[6:10]
    content = ''.join(filter(lambda l: l != '\0', str(packet[10:])))

    return id_sequence, packet_type, timestamp, content
