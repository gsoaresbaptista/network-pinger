from abc import ABC, abstractmethod
from typing import Tuple
import os
import datetime
import socket


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
