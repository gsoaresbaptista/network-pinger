from package import get_timestamp


def create_package(package_id: str, package_type: str, message: str) -> bytes:
    '''Generate a standard-compliant package
    In order, the package consists of:
        - 5 bytes, sequence number
        - 1 byte, ping = 0 or pong = 1
        - 4 bytes, timestamp
        - 30 bytes, package content
    :param package_id - int, sequence number
    :param package_type - int, 0 to ping and 1 to pong
    :param message - str, package content
    :return package - bytes, package as byte stream
    '''
    # TODO: Check params
    id_str = package_id.rjust(5, '0')
    ping_std = package_type  # 0 = ping, 1 = pong
    timestamp = get_timestamp()  # initial timestamp
    package_message = id_str + ping_std + timestamp + message.ljust(30, '\0')
    return package_message.encode('ascii')
