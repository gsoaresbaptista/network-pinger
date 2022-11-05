from abc import ABC, abstractmethod
from typing import Dict, Tuple
import os
import sys
import datetime
import socket
from ping.package import create_package, read_package


class AbstractServer(ABC):
    '''Assign Interface Contracts to a server object.'''

    def __init__(self, timeout: float | int = 5) -> None:
        super().__init__()
        # set initial environment
        os.environ["TZ"] = "UTC"
        self._address: Tuple[str, int]
        self._connection: socket.socket
        self._timeout = timeout

    @abstractmethod
    def connect(self, server_ip: str, server_port: int) -> None:
        '''Hosts server on server_ip on server_port.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''

    @abstractmethod
    def disconnect(self) -> None:
        '''Close server connection.
        :param None
        :return None
        '''

    @abstractmethod
    def check(self) -> Dict[str, int | float | str]:
        '''Return server state.
        :param None
        :return None
        '''

    def listen(self) -> None:
        '''Makes the server listen and expect to receive some data.
        :param None
        :return None
        '''
        running: bool = True

        try:
            while running:
                self._listen_one()
                sys.stdout.flush()
        except KeyboardInterrupt:
            self.disconnect()

    def emmit(self, category: str, message: str) -> None:
        '''Emmit a message to standart output.
        :param message - str, text to emmit
        :return None
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{now} - {category:4} | {message}")

    # private methods, using defined pattern for packages
    def _listen_one(self) -> None:
        '''Procedure to handle a packaged in the defined pattern.
        :param None
        :return None
        '''
        byte_stream, received_address = self._connection.recvfrom(40)
        address = f"{received_address[0]}:{received_address[1]}"
        self._create_response(byte_stream)
        self.emmit('RECV', f"package received from {address}")

    def _create_response(self, byte_stream: bytes) -> bytes:
        '''.'''
        package = byte_stream.decode('ascii')
        sid, ptype, time, content = read_package(package)
        # TODO: Check if is ping
        response = create_package(sid, 1, content)
        return response
