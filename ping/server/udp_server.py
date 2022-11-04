import socket
from typing import Dict, Union, Tuple
from server.server_interface import ServerInterface


class UDPServer(ServerInterface):
    '''UDP server implementation'''

    def __init__(self) -> None:
        super().__init__()
        self.__address: Tuple[str, int]
        self.__connection: socket.socket
        self.emmit('UDP Server initialized')

    def connect(self, server_ip: str, server_port: int) -> None:
        '''Hosts server on server_ip on server_port.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''
        self.__address = (server_ip, server_port)
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connection.bind(self.__address)
        self.emmit(f"Running on {server_ip}:{server_port}")

    def disconnect(self) -> None:
        '''Close server connection.
        :param None
        :return None
        '''
        self.__connection.close()
        self.emmit('Server connection closed')

    def check(self) -> Dict[str, Union[int, float, str]]:
        '''Return server state.
        :param None
        :return None
        '''
        return {
            'server_ip': self.__address[0],
            'server_port': self.__address[1],
        }
