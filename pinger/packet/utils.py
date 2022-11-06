import time
from typing import Tuple


def get_timestamp() -> str:
    '''Get current timestamp in string format
    :param None
    : return timestamp - str, last four digits of unix time
    '''
    return str(get_int_timestamp()).rjust(4, '0')


def get_int_timestamp() -> int:
    '''Get current timestamp
    On Windows and most Unix systems, the timestamp is the last four
    time numbers in seconds since the epoch (Unix time).
    :param None
    : return timestamp - int, last four digits of unix time
    '''
    return int((time.time() / 10 % 1) * 10000)


def check_packet(sid: str, ptype: str, timestamp: str, content: str, ping_expected: bool) -> Tuple[bool, str | None]:
    '''Check packet consistency
    :param sid - str, sequence number
    :param ptype - char, 0 to ping and 1 to pong
    :param timestamp - str, packet timestamp
    :param content - str, packet content
    :param ping_expected - bool, True if ping is expected, otherwise False
    :return True if it passes all integrity conditions, False otherwise
    '''
    if not sid.isnumeric():
        return False, f"Non numeric sequence number {'sent' if ping_expected else 'received'}"
    if (ptype != '0' and ping_expected) or (ptype != '1' and not ping_expected):
        return False, f"Ping-pong {'sent' if ping_expected else 'received'} incorrectly"
    if not timestamp.isnumeric():
        return False, f"Non numeric timestamp {'sent' if ping_expected else 'received'}"
    if len(content) > 30:
        return False, 'Larger content than allowed'
    return True, None
