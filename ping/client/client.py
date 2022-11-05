import socket
import time
import random
import string


def get_timestamp() -> int:
    '''Get current timestamp
    On Windows and most Unix systems, the timestamp is the last four
    time numbers in seconds since the epoch (Unix time).
    :param None
    : return timestamp - int, last four digits of unix time
    '''
    return round(time.time()) % 10000


def create_message(package_id: int, message: str) -> bytes:
    '''Generate a standard-compliant package
    In order, the package consists of:
        - 5 bytes, sequence number
        - 1 byte, ping = 0 or pong = 1
        - 4 bytes, timestamp
        - 30 bytes, package content
    :param package_id - int, sequence number
    :param message - str, package content
    :return package - bytes, package as byte stream
    '''
    id_str = str(package_id).rjust(5, '0')
    ping_std = '0'  # 0 = ping, 1 = pong
    timestamp = str(get_timestamp())  # initial timestamp
    package_message = id_str + ping_std + timestamp + message.ljust(30, '\0')
    return package_message.encode('utf8')


# generate message
content_size = random.randint(1, 30)
CONTENT = ''.join(random.choices(string.ascii_lowercase, k=content_size))

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(create_message(0, CONTENT), ('127.0.0.1', 3000))
