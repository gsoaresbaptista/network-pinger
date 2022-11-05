import socket


def create_message(package_id: int, message: str) -> bytes:
    '''.'''
    id_str = str(package_id).ljust(5, '0')
    ping_std = '0'  # 0 = ping, 1 = pong
    timestamp = '0000'  # initial timestamp is zero
    package_message = id_str + ping_std + timestamp + message.rjust(30, '\0')
    return package_message.encode('utf8')


udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(create_message(0, 'batata'), ('127.0.0.1', 3000))
