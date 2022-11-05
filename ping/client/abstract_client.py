from abc import ABC, abstractmethod
from typing import Dict, Tuple
import os
import sys
import datetime
import socket
from package import create_package, read_package


class AbstractClient(ABC):
    '''Assign Interface Contracts to a client object.'''

    def __init__(
        self, server_ip: str, server_port: int, timeout: float | int = 5
    ) -> None:
        '''Create a client for a specific server.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''
        super().__init__()
        # set initial environment
        os.environ["TZ"] = "UTC"
        self._timeout = timeout
        self._socket: socket.socket
        self._server_address = (server_ip, server_port)
        self._sent_package: Tuple[str, str, str, str]

    @abstractmethod
    def connect(self) -> None:
        '''Initialize client connections.
        :param None
        :return None
        '''

    @abstractmethod
    def send_to_server(
        self, seqid: str = '0', message: str | None = None
    ) -> None:
        '''.'''

    @abstractmethod
    def wait_response(self) -> None:
        '''.'''

    @abstractmethod
    def disconnect(self) -> None:
        '''Close client connection.
        :param None
        :return None
        '''

    @staticmethod
    def emmit(category: str, message: str) -> None:
        '''Emmit a message to standart output.
        :param message - str, text to emmit
        :return None
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{now} - {category:5} | {message}")

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
            AbstractClient.emmit('ERROR', 'Non numeric sequence number')
            return False
        if ptype != '0':
            AbstractClient.emmit('ERROR', 'Received pong instead of ping')
            return False
        if not time.isnumeric():
            AbstractClient.emmit('ERROR', 'Non numeric timestamp')
            return False
        if len(content) > 30:
            AbstractClient.emmit('ERROR', 'Larger content than allowed')
            return False
        return True