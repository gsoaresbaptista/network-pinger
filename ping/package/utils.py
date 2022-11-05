import time
from typing import Tuple


def get_timestamp() -> str:
    '''Get current timestamp
    On Windows and most Unix systems, the timestamp is the last four
    time numbers in seconds since the epoch (Unix time).
    :param None
    : return timestamp - int, last four digits of unix time
    '''
    return str(round(time.time()))[-4:]


def check_package(
    sid: str, ptype: str, timestamp: str, content: str
) -> Tuple[bool, str | None]:
    '''Check package consistency
    :param sid - str, sequence number
    :param ptype - char, 0 to ping and 1 to pong
    :param timestamp - str, package timestamp
    :param content - str, package content
    :return True if it passes all integrity conditions, False otherwise
    '''
    if not sid.isnumeric():
        return False, 'Non numeric sequence number'
    if ptype != '0':
        return False, 'Received pong instead of ping'
    if not timestamp.isnumeric():
        return False, 'Non numeric timestamp'
    if len(content) > 30:
        return False, 'Larger content than allowed'
    return True, None
