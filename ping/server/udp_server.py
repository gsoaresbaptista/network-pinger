import socket
from typing import Dict
from server.abstract_server import AbstractServer


class UDPServer(AbstractServer):
    '''UDP server implementation'''

    def __init__(self) -> None:
        super().__init__()
        self.emmit('INIT', 'UDP Server initialized')

    def connect(self, server_ip: str, server_port: int) -> None:
        '''Hosts server on server_ip on server_port.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''
        # creating socket to receive
        self._address = (server_ip, server_port)
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._connection.bind(self._address)
        self.emmit('INIT', f"Listen packages on {server_ip}:{server_port}")
        # creating socket to send
        self._response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.emmit('INIT', 'Response socket created')

    def disconnect(self) -> None:
        '''Close server connection.
        :param None
        :return None
        '''
        self._connection.close()
        self._response_socket.close()
        self.emmit('END', 'Server connection closed')

    def check(self) -> Dict[str, int | float | str]:
        '''Return server state.
        :param None
        :return None
        '''
        return {
            'server_ip': self._address[0],
            'server_port': self._address[1],
            'timeout_time': self._timeout,
        }
