from abc import ABC, abstractmethod
from typing import Tuple, List
import os
import sys
import datetime
import socket
from io import TextIOWrapper
from utils import merge_alternatively, join_list


class AbstractClient(ABC):
    '''Assign Interface Contracts to a client object.'''

    def __init__(
        self,
        server_ip: str,
        server_port: int,
        timeout: float | int,
        save_csv: bool = False,
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
        self._received_package: Tuple[str, str, str, str]
        self._sent = 0
        self._lost = 0
        self._total = 0
        self._times: List[float] = []
        self._csv: TextIOWrapper | None
        self._create_csv(save_csv)

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
    def wait_response(self) -> float | None:
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

    def _create_csv(self, save_csv: bool) -> None:
        '''.'''

        if save_csv:
            self._csv = open('packages_data.csv', 'w', encoding='utf8')
            self._write_csv_list(
                join_list(
                    ['sid', 'type', 'timestamp', 'message'],
                    ['sent', 'received'],
                ),
            )
            self._csv.write(',rtt\n')
        else:
            self._csv = None

    def run(self) -> None:
        '''.'''
        for i in range(10):
            self.send_to_server(str(i))
            rtt = self.wait_response()

            # fix rtt if timestamp exceeds limit
            if rtt is not None and rtt < 0:
                rtt += 10000.0

            if self._csv is not None:
                self._write_csv_list(
                    merge_alternatively(
                        self._sent_package, self._received_package
                    )
                )
                self._csv.write(f",{str(rtt)}\n")
                self._csv.flush()

            # force emmits to stdout
            sys.stdout.flush()
        self.disconnect()

        if self._csv is not None:
            self._csv.close()

    def _write_csv_list(self, line: List[str]) -> None:
        '''.'''
        if self._csv is not None:
            self._csv.write(','.join(line))
