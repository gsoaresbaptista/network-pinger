from abc import ABC, abstractmethod
from typing import Dict, Union, Tuple
import os
import datetime
import socket


class ServerInterface(ABC):
    '''Assign Interface Contracts to a server object.'''

    def __init__(self, timeout: Union[float, int] = 5) -> None:
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
    def check(self) -> Dict[str, Union[int, float, str]]:
        '''Return server state.
        :param None
        :return None
        '''

    @abstractmethod
    def listen(self) -> None:
        '''Makes the server listen and expect to receive some data.'''

    def emmit(self, message: str) -> None:
        '''Emmit a message to standart output.
        :param message - str, text to emmit'''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        print(f"{now} - {type(self).__name__} | {message}")
