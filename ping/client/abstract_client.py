from abc import ABC, abstractmethod
from typing import Tuple, List
import os
import sys
import time
import datetime
import socket
from io import TextIOWrapper
from statistics import mean, stdev
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
        self._sent_packet: Tuple[str, str, str, str]
        self._received_packet: Tuple[str, str, str, str]
        self._sent = 0
        self._received = 0
        self._rtts: List[float] = []
        self._initial_time = time.time()
        self._csv: TextIOWrapper | None
        self._create_csv(save_csv)
        self.emmit('INIT', 'UDP Client initialized')

    @abstractmethod
    def connect(self) -> None:
        '''Initialize client connections.
        :param None
        :return None
        '''

    @abstractmethod
    def send_to_server(self, seqid: str = '0', message: str | None = None) -> Tuple[str, int]:
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
            self._csv = open('packets_data.csv', 'w', encoding='utf8')
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
            server_ip, server_port = self.send_to_server(str(i))
            address = f"{server_ip}:{server_port}"
            self._sent += 1
            self.emmit('SENT', f"Message sent to server {address}")

            # wait for server response
            rtt = self.wait_response()

            if rtt is not None:
                # fix rtt if timestamp exceeds limit
                rtt += 10000.0 if rtt < 0 else 0
                self._rtts.append(rtt)
                self._received += 1
                # emmit message
                self.emmit(
                    'RECV',
                    f'Reply received successfully, rtt = {int(rtt)}ms',
                )
            else:
                self.emmit('ERROR', 'packet was lost')

            if self._csv is not None:
                self._write_csv_list(merge_alternatively(self._sent_packet, self._received_packet))
                self._csv.write(f",{str(rtt)}\n")
                self._csv.flush()

            # force emmits to stdout
            sys.stdout.flush()

        self._summary()
        self.disconnect()

        if self._csv is not None:
            self._csv.close()

    def _summary(self) -> None:
        '''.'''
        rtt_min = min(self._rtts)
        rtt_avg = mean(self._rtts)
        rtt_max = max(self._rtts)
        rtt_std = stdev(self._rtts)

        print('-' * 70)
        self.emmit_info(f"Total time = {time.time() - self._initial_time:.4f} seconds")
        self.emmit_info(f"{self._sent} packets transmitted, {self._received} received.")
        self.emmit_info(f"{100*(self._sent - self._received)/self._sent:.2f}% packet loss.")
        self.emmit_info(f"rtt min/avg/max/mdev = {rtt_min:.3f}/{rtt_avg:.3f}/{rtt_max:.3f}/{rtt_std:.3f} ms")
        print('-' * 70)

    def _write_csv_list(self, line: List[str]) -> None:
        '''.'''
        if self._csv is not None:
            self._csv.write(','.join(line))

    def emmit_info(self, message: str) -> None:
        '''.'''
        self.emmit('INFO', message)
