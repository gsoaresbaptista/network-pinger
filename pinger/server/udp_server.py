import socket
from typing import Tuple
from server.abstract_server import AbstractServer


class UDPServer(AbstractServer):
    '''UDP server implementation'''

    def __init__(
        self,
        timeout: float | int,
    ) -> None:
        super().__init__(timeout)
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
        self.emmit('INIT', f"Listen packets on {server_ip}:{server_port}")
        # creating socket to send
        self._response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.emmit('INIT', 'Response socket created')
        # set maximum time without request
        self._connection.settimeout(self._timeout)
        self.emmit('INFO', f'Set {self._timeout} seconds as maximum no-request time')

    def disconnect(self) -> None:
        '''Close server connection.
        :param None
        :return None
        '''
        self._connection.close()
        self._response_socket.close()
        self.emmit('END', 'Server connection closed')

    def _send_reply(self, reply: bytes | None, address: Tuple[str, int]) -> None:
        '''Send a response to a client requisition.
        :param reply - bytes, received requisition
        :param address - Tuple[str, int], server address and server port
        :return None
        '''
        if reply is not None:
            self._response_socket.sendto(reply, address)

    def _listen_one(self) -> Tuple[bytes | None, Tuple[str, int]]:
        '''Procedure to handle a packetd in the defined pattern.
        :param None
        :return Tuple[str, int] - Tuple with response packet and client address
        '''
        byte_stream, received_address = self._connection.recvfrom(1024)
        response: bytes | None = self._create_response(byte_stream)
        return response, received_address
