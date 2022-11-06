import socket
import random
import string
from typing import Tuple
from packet import create_packet, read_packet, check_packet, get_timestamp
from .abstract_client import AbstractClient


class UDPClient(AbstractClient):
    '''UDP client implementation'''

    def __init__(
        self,
        server_ip: str,
        server_port: int,
        timeout: float | int,
        number_of_packets: int = 10,
        save_csv: bool = False,
    ) -> None:
        super().__init__(server_ip, server_port, timeout, number_of_packets, save_csv)
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

    def send_to_server(self, seqid: str = '0', message: str | None = None) -> Tuple[str, int]:
        '''Send a packet to connected server.
        :param seqid - str, sequence number
        :param message - str or None, if None a random message is generated
        :return server_address - Tuple[str, int], server_address, server_port
        '''
        # generate message
        if message is None:
            content_size = random.randint(1, 30)
            message = ''.join(random.choices(string.ascii_lowercase, k=content_size))

        # send message to server
        packet = create_packet(seqid, '0', None, message)
        self._socket.sendto(packet, self._server_address)

        # save the sent packet to compare with the response
        self._sent_packet = read_packet(packet.decode('ascii'))

        return self._server_address

    def wait_response(self) -> float | None:  # type: ignore
        '''Make client wait for a response from the server.
        :param None
        :return float or None - rrt computed or None if there is an error
                                or inconsistency response
        '''
        valid = False

        try:
            while not valid:
                response, _ = self._socket.recvfrom(1024)
                sid, ptype, time, content = read_packet(response.decode('ascii'))
                valid, message = check_packet(sid, ptype, time, content, False)

                # compare received packet with the last sent one
                if valid:
                    valid = sid == self._sent_packet[0]
                    message = 'Sequence id is not the same'

                if not valid:
                    AbstractClient.emmit('ERROR', str(message))
                    self._received_packet = ('0000', '0', '0000', 'ERROR')
                    return None
                else:
                    # save the received packet to compare
                    current_time = get_timestamp()
                    self._received_packet = (sid, ptype, current_time, content)
                    return float(current_time) - float(time)
        except TimeoutError:
            # save the last received packet to compare
            self._received_packet = ('0000', '0', '0000', 'TIMEOUTERROR')

            return None
