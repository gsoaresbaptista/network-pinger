from abc import ABC, abstractmethod
from typing import Dict, Tuple
import os
import sys
import datetime
import socket
from package import create_package, read_package


class AbstractServer(ABC):
    '''Assign Interface Contracts to a server object.'''

    def __init__(self, timeout: float | int = 5) -> None:
        super().__init__()
        # set initial environment
        os.environ["TZ"] = "UTC"
        self._address: Tuple[str, int]
        self._connection: socket.socket
        self._timeout = timeout
        self._response_socket: socket.socket

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

    @staticmethod
    def emmit(category: str, message: str) -> None:
        '''Emmit a message to standart output.
        :param message - str, text to emmit
        :return None
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{now} - {category:5} | {message}")

    # private methods, using defined pattern for packages
    def _listen_one(self) -> None:
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
        if response is not None:
            self._response_socket.sendto(response, received_address)

    @staticmethod
    def _check_package_state(
        sid: str, ptype: str, time: str, content: str
    ) -> bool:
        '''Check package consistency
        :param sid - str, sequence number
        :param ptype - char, 0 to ping and 1 to pong
        :param time - str, timestamp
        :param content - str, package content
        :return True if it passes all integrity conditions, False otherwise
        '''
        if not sid.isnumeric():
            AbstractServer.emmit('ERROR', 'Non numeric sequence number')
            return False
        if ptype != '0':
            AbstractServer.emmit('ERROR', 'Received pong instead of ping')
            return False
        if not time.isnumeric():
            AbstractServer.emmit('ERROR', 'Non numeric timestamp')
            return False
        if len(content) > 30:
            AbstractServer.emmit('ERROR', 'Larger content than allowed')
            return False
        return True

    @staticmethod
    def _create_response(byte_stream: bytes) -> bytes | None:
        '''Make a response to received package
        :param byte_stream - bytes, package received
        :return bytes if packet is consistent otherwise None
        '''
        package = byte_stream.decode('ascii')
        sid, ptype, time, content = read_package(package)
        valid = AbstractServer._check_package_state(sid, ptype, time, content)
        response: bytes = create_package(sid, '1', content)
        return response if valid else None
