import argparse
from client import UDPClient


if __name__ == '__main__':
    # arguments
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
        description="Run a client to send ping and receive pong as well as calculate rtt.",
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
        help='Save all package data in a csv file.',
        action='store_true',
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help=(
            'Set how long to wait for a client to receive a '
            'response before receiving a timeout, in seconds.'
        ),
        action='store',
        default=3,
    )
    args = parser.parse_args()

    client = UDPClient('127.0.0.1', 3000, int(args.timeout), args.csv)
    client.run()
    # client.send_to_server()
    # client.wait_response()
