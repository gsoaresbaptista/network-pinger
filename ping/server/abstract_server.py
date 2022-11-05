from abc import ABC, abstractmethod
from typing import Dict, Tuple
import os
import sys
import datetime
import socket


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
        print(f"{now} - {category:5} | {message}")

    # private methods, using defined pattern for packages
    def _handle_package(self, package: str) -> Tuple[int, int, int, str]:
        '''Handle a standard-compliant package
        Unpack all package data into single variables
        :param package - str, packet decoded in ascii format
        :return
            - id_sequence - int, sequence number
            - package_type - int, 0 if ping or 1 for pong
            - timestamp - int, timestamp in seconds
            - content - str, package content
        '''
        id_sequence = int(package[:5])
        package_type = int(package[5])
        timestamp = int(package[6:10])
        content = package[10:]

        return id_sequence, package_type, timestamp, content

    def _listen_one(self) -> None:
        '''Procedure to handle a packaged in the defined pattern.
        :param None
        :return None
        '''
        package, received_address = self._connection.recvfrom(64)
        address = f"{received_address[0]}:{received_address[1]}"
        package = package.decode('ascii')
        seq, req, timestamp, content = self._handle_package(package)
        self.emmit('RECV', f"'{content}' received from {address}")
