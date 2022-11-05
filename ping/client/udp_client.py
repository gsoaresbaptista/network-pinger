import socket
import random
import string
from typing import Dict
from package import create_package, read_package, check_package, get_timestamp
from .abstract_client import AbstractClient


class UDPClient(AbstractClient):
    '''UDP client implementation'''

    def __init__(
        self,
        server_ip: str,
        server_port: int,
        timeout: float | int = 5,
        save_csv: bool = False,
    ) -> None:
        super().__init__(server_ip, server_port, timeout, save_csv)
        self.emmit('INIT', 'UDP Client initialized')
        self.connect()

    def connect(self) -> None:
        '''Create a client for a specific server.
        :param server_ip - str, machine ipv4
        :param server_pot - int, port to host server
        :return None
        '''
        # initializing socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._timeout)
        self.emmit('INIT', "Socket created")

    def disconnect(self) -> None:
        '''Close client connection.
        :param None
        :return None
        '''
        self._socket.close()
        self.emmit('END', 'Client socket closed')

    def check(self) -> Dict[str, int | float | str]:
        '''Return client state.
        :param None
        :return None
        '''
        return {
            'connected_server_ip': self._server_address[0],
            'connected_server_port': self._server_address[1],
            'timeout_time': self._timeout,
        }

    def send_to_server(
        self, seqid: str = '0', message: str | None = None
    ) -> None:
        '''.'''
        # generate message
        if message is None:
            content_size = random.randint(1, 30)
            message = ''.join(
                random.choices(string.ascii_lowercase, k=content_size)
            )

        # send message to server
        package = create_package(seqid, '0', message)
        self._socket.sendto(package, self._server_address)

        # save the sent package to compare with the response
        self._sent_package = read_package(package.decode('ascii'))

        # emmit message
        server_ip, server_port = self._server_address
        self.emmit('SENT', f"Message sent to server {server_ip}:{server_port}")

    def wait_response(self) -> float | None:  # type: ignore
        '''.'''
        valid = False

        try:
            while not valid:
                response, _ = self._socket.recvfrom(1024)
                sid, ptype, time, content = read_package(
                    response.decode('ascii')
                )
                valid, message = check_package(sid, ptype, time, content, False)

                # compare received package with the last sent one
                valid = sid == self._sent_package[0]
                message = 'Sequence id is not the same'

                if not valid:
                    AbstractClient.emmit('ERROR', str(message))
                else:
                    AbstractClient.emmit('RECV', 'Reply received successfully')
                    # save the received package to compare
                    current_time = get_timestamp()
                    self._received_package = (sid, ptype, current_time, content)

                    return float(current_time) - float(time)
        except TimeoutError:
            AbstractClient.emmit('ERROR', 'Timeout waiting for response')
            # save the last received package to compare
            self._received_package = ('0000', '0', '0000', 'TIMEOUTERROR')

            return None
