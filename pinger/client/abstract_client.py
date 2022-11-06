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
        number_of_packets: int = 10,
        save_csv: bool = False,
    ) -> None:
        '''Create a client for a specific server.
        :param server_ip - str, machine ipv4
        :param server_port - int, port to host server
        :param timeout - int | float, time in seconds client waits for response
        :param number_ob_packets - int, number of packets to send
        :param save_csv - bool, True to save sent and received packet data in csv file
        :return None
        '''
        super().__init__()
        # set initial environment
        os.environ["TZ"] = "UTC"
        self._timeout = timeout
        self._socket: socket.socket
        self._server_address = (server_ip, server_port)
        self._sent_packet: Tuple[str, str, str, str]
        self._received_packet: Tuple[str, str, str, str] = None
        self._sent = 0
        self._received = 0
        self._rtts: List[float] = []
        self._initial_time = time.time()
        self._csv: TextIOWrapper | None
        self._number_of_packets = number_of_packets
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
        '''Send a packet to connected server.
        :param seqid - str, sequence number
        :param message - str or None, if None a random message is generated
        :return server_address - Tuple[str, int], server_address, server_port
        '''

    @abstractmethod
    def wait_response(self) -> float | None:
        '''Make client wait for a response from the server.
        :param None
        :return None
        '''

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
        '''Create the csv file with sent and received packets and rtt data.
        :param save_csv - bool, True if yout want create a csv file, otherwise False
        :return None
        '''
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
        '''Run client pipeline.

        Make server send a message to the connected server and wait for a valid response.
        :param None
        :return None
        '''
        for i in range(self._number_of_packets):
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
            elif self._received_packet and self._received_packet[3] == 'TIMEOUTERROR':
                self.emmit('ERROR', 'Timeout waiting for response, packet was lost')

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
        '''Emmit the summary with some statistics about the packets sent and received.
        :param None
        :return None
        '''
        rtt_min = min(self._rtts) if len(self._rtts) > 0 else 0
        rtt_avg = mean(self._rtts) if len(self._rtts) > 0 else 0
        rtt_max = max(self._rtts) if len(self._rtts) > 0 else 0
        rtt_std = stdev(self._rtts) if len(self._rtts) > 0 else 0

        print('-' * 70)
        self.emmit_info(f"Total time = {time.time() - self._initial_time:.4f} seconds")
        self.emmit_info(f"{self._sent} packets transmitted, {self._received} received.")
        self.emmit_info(f"{100*(self._sent - self._received)/(self._sent if self._sent > 0 else 1):.2f}% packet loss.")
        self.emmit_info(f"rtt min/avg/max/mdev = {rtt_min:.3f}/{rtt_avg:.3f}/{rtt_max:.3f}/{rtt_std:.3f} ms")
        print('-' * 70)

    def _write_csv_list(self, line: List[str]) -> None:
        '''Trick to write list in csv file.

        Note that each items in the list is a specific column in csv.
        :param line - List[str], list with string data to write in csv file
        :return None
        '''
        if self._csv is not None:
            self._csv.write(','.join(line))

    def emmit_info(self, message: str) -> None:
        '''Trick to emmit a info message
        :param message - str, message to print in stdout
        :return None
        '''
        self.emmit('INFO', message)
