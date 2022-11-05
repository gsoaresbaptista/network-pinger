import sys
import argparse
from server import Server, UDPServer


if __name__:
    # arguments
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
        description=(
            "Run a server to receive ping and respond "
            "with pong to compute rtt."
        ),
    )
    parser.add_argument(
        "-l",
        "--logger",
        help='Save all server output in log file.',
        action='store_true',
    )
    args = parser.parse_args()

    # stdout change
    if args.logger:
        previous = sys.stdout
        sys.stdout = open('log.txt', 'a', encoding='utf8')

    # server run
    server: Server = UDPServer()
    server.connect('127.0.0.1', 3000)
    server.listen()

    # revert stdout change
    if args.logger:
        sys.stdout.close()
        sys.stdout = previous
