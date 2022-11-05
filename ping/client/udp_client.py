import socket
import random
import string
from typing import Dict
from client.abstract_client import AbstractClient
from package import create_package, read_package


class UDPClient(AbstractClient):
    '''UDP client implementation'''

    def __init__(
        self, server_ip: str, server_port: int, timeout: float | int = 5
    ) -> None:
        super().__init__(server_ip, server_port, timeout)
        self.emmit('INIT', 'UDP Client initialized')
        self.connect()

    def connect(self) -> None:
        '''Create a client for a specific server.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''
        # initializing socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._timeout)
        self.emmit('INIT', "Socket created")

    def disconnect(self) -> None:
        '''Close client connection.
        :param None
        :return None
        '''
        self._socket.close()
        self.emmit('END', 'Client socket closed')

    def check(self) -> Dict[str, int | float | str]:
        '''Return client state.
        :param None
        :return None
        '''
        return {
            'connected_server_ip': self._server_address[0],
            'connected_server_port': self._server_address[1],
            'timeout_time': self._timeout,
        }

    def send_to_server(
        self, seqid: str = '0', message: str | None = None
    ) -> None:
        '''.'''
        # generate message
        if message is None:
            content_size = random.randint(1, 30)
            message = ''.join(
                random.choices(string.ascii_lowercase, k=content_size)
            )

        # send message to server
        package = create_package(seqid, '0', message)
        self._socket.sendto(package, self._server_address)

        # save the sent package to compare with the response
        self._sent_package = read_package(package.decode('ascii'))

        # emmit message
        server_ip, server_port = self._server_address
        self.emmit('SENT', f"Message sent to server {server_ip}:{server_port}")

    def wait_response(self) -> None:
        '''.'''
        response, _ = self._socket.recvfrom(1024)
        print(read_package(response.decode('ascii')))
