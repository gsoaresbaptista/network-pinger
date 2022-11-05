from typing import Tuple


def read_package(package: str) -> Tuple[int, int, int, str]:
    '''Handle a standard-compliant package
    Unpack all package data into single variables
    :param package - str, packet decoded in ascii format
    :return
        - id_sequence - int, sequence number
        - package_type - int, 0 if ping or 1 for pong
        - timestamp - int, timestamp in seconds
        - content - str, package content
    '''
    id_sequence = int(package[:5])
    package_type = int(package[5])
    timestamp = int(package[6:10])
    content = package[10:]

    return id_sequence, package_type, timestamp, content
