import argparse
import sys
from client import UDPClient


if __name__ == '__main__':
    # arguments
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
        description="Run a client to send ping and receive pong as well as calculate rtt.",
    )
    parser.add_argument(
        "-ip",
        "--server_ip",
        help=('Set the IP address that the client will connect. Default is 127.0.0.1.'),
        action='store',
        default='127.0.0.1',
    )
    parser.add_argument(
        "-port",
        "--server_port",
        help=('Set the port that the client will connect. Default is 3000.'),
        action='store',
        default=3000,
    )
    parser.add_argument(
        "-l",
        "--logger",
        help='Save all client output in log file.',
        action='store_true',
    )
    parser.add_argument(
        "-c",
        "--csv",
        help='Save all packet data in a csv file.',
        action='store_true',
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help=('Set how long to wait for a client to receive a ' 'response before receiving a timeout, in seconds.'),
        action='store',
        default=10,
    )
    parser.add_argument(
        "-p",
        "--packets",
        help=('Number of packets to send.'),
        action='store',
        default=10,
    )
    args = parser.parse_args()

    # stdout change
    if args.logger:
        previous = sys.stdout
        sys.stdout = open('client_log.txt', 'w', encoding='utf8')

    client = UDPClient(
        server_ip=args.server_ip,
        server_port=int(args.server_port),
        timeout=int(args.timeout),
        number_of_packets=int(args.packets),
        save_csv=args.csv,
    )
    client.run()

    # revert stdout change
    if args.logger:
        sys.stdout.close()
        sys.stdout = previous
