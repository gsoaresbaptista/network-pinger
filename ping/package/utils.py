import time


def get_timestamp() -> str:
    '''Get current timestamp
    On Windows and most Unix systems, the timestamp is the last four
    time numbers in seconds since the epoch (Unix time).
    :param None
    : return timestamp - int, last four digits of unix time
    '''
    return str(round(time.time()))[-4:]