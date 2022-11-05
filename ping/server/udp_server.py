import socket
from typing import Dict, Tuple
from server.abstract_server import AbstractServer
from package import get_int_timestamp


class UDPServer(AbstractServer):
    '''UDP server implementation'''

    def __init__(self) -> None:
        super().__init__()
        self.emmit('INIT', 'UDP Server initialized')
        self._configurations = {'simulate_delay': True}

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
        }

    def _send_reply(
        self, reply: bytes | None, address: Tuple[str, int]
    ) -> None:
        '''.'''
        if reply is not None:
            self._response_socket.sendto(reply, address)

    def _listen_one(self) -> Tuple[bytes | None, Tuple[str, int]]:
        '''Procedure to handle a packaged in the defined pattern.
        :param None
        :return None
        '''
        # receiving
        byte_stream, received_address = self._connection.recvfrom(1024)
        address = f"{received_address[0]}:{received_address[1]}"
        self.emmit('RECV', f"package received from {address}")
        # responding
        response: bytes | None = self._create_response(byte_stream)
        return response, received_address

    def _simulations(self, response: bytes | None) -> None:
        '''.'''
        if response is not None:
            if self._configurations['simulate_delay']:
                wait_time = 1000
                while get_int_timestamp() - int(response[6:10]) < wait_time:
                    continue
