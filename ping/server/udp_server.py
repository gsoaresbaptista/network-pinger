import socket
from typing import Dict, Union
from server.abstract_server import AbstractServer


class UDPServer(AbstractServer):
    '''UDP server implementation'''

    def __init__(self, timeout: Union[float, int] = 5) -> None:
        super().__init__(timeout)
        self.emmit('UDP Server initialized')

    def connect(self, server_ip: str, server_port: int) -> None:
        '''Hosts server on server_ip on server_port.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''
        self._address = (server_ip, server_port)
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._connection.settimeout(self._timeout)
        self._connection.bind(self._address)
        self.emmit(f"Running on {server_ip}:{server_port}")

    def disconnect(self) -> None:
        '''Close server connection.
        :param None
        :return None
        '''
        self._connection.close()
        self.emmit('Server connection closed')

    def check(self) -> Dict[str, Union[int, float, str]]:
        '''Return server state.
        :param None
        :return None
        '''
        return {
            'server_ip': self._address[0],
            'server_port': self._address[1],
            'timeout_time': self._timeout,
        }

    def listen(self) -> None:
        '''.'''
        message, address = self._connection.recvfrom(40)
        address = f"{address[0]}:{address[1]}"
        self.emmit(f"'{message.decode('utf8')}' received from {address}")
