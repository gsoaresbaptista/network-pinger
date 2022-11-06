from abc import ABC, abstractmethod
from typing import Dict, Tuple
import os
import sys
import datetime
import socket
from packet import create_packet, read_packet, check_packet


class AbstractServer(ABC):
    '''Assign Interface Contracts to a server object.'''

    def __init__(
        self,
        timeout: float | int,
    ) -> None:
        super().__init__()
        # set initial environment
        os.environ["TZ"] = "UTC"
        self._address: Tuple[str, int]
        self._connection: socket.socket
        self._response_socket: socket.socket
        self._configurations: Dict[str, bool | int | float | str] = {}
        self._timeout = timeout
        self._settings = {'simulate_delay': False, 'simulate_loss': False}

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

    @abstractmethod
    def _listen_one(self) -> Tuple[bytes | None, Tuple[str, int]]:
        '''Procedure to handle a packetd in the defined pattern.
        :param None
        :return None
        '''

    @abstractmethod
    def _send_reply(self, reply: bytes | None, address: Tuple[str, int]) -> None:
        '''Send a response to a client requisition.
        :param reply - bytes, received requisition
        :param address - Tuple[str, int], server address and server port
        :return None
        '''

    def set_setting(self, key: str, value: int | float | str | bool) -> None:
        '''Set a server setting to a new value provided.
        :param key - str, parameter to change
        :param value - int | float | str | bool, new parameter value
        :return None
        '''
        self._settings[key] = value

    def listen(self) -> None:
        '''Makes the server listen and expect to receive some data.
        :param None
        :return None
        '''
        running: bool = True

        try:
            while running:
                response, address = self._listen_one()

                # emmit received
                self.emmit(
                    'RECV',
                    f"packet received from {f'{address[0]}:{address[1]}'}",
                )

                response = self._simulations(response)
                self._send_reply(response, address)

                # emmit sent
                self.emmit(
                    'SENT',
                    f"response sent to {f'{address[0]}:{address[1]}'}",
                )

                # force emmits to stdout
                sys.stdout.flush()
        except KeyboardInterrupt:
            self.disconnect()
        except TimeoutError:
            self.emmit(
                'ERROR',
                f'Maximum no-request time of {self._timeout} seconds exceeded',
            )
            self.disconnect()

    def emmit_setting(self) -> None:
        '''Emmit a server setting to stdout.

        Print all server settings in the configured stdout.
        :param None
        :return None
        '''
        print('-' * 60)
        for key, value in self._settings.items():
            self.emmit('CONFG', f'Setting {key} set as {value}')
        print('-' * 60)

    @staticmethod
    def emmit(category: str, message: str) -> None:
        '''Emmit a message to standart output.
        :param message - str, text to emmit
        :return None
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{now} - {category:5} | {message}")

    @staticmethod
    def _create_response(byte_stream: bytes) -> bytes | None:
        '''Make a response to received packet
        :param byte_stream - bytes, packet received
        :return bytes if packet is consistent otherwise None
        '''
        packet = byte_stream.decode('ascii')
        sid, ptype, time, content = read_packet(packet)
        valid, message = check_packet(sid, ptype, time, content, True)

        if valid:
            return create_packet(sid, '1', time, content)

        AbstractServer.emmit('ERROR', str(message))
        return None

    def _simulations(self, response: bytes | None) -> bytes | None:
        '''Compute all simulations that are enabled.
        :param response - bytes, response packet, passed to change in simulations
        :return bytes | none, new response packet
        '''
