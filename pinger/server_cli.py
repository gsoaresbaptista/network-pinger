import sys
import argparse
from server import Server, UDPServer


if __name__ == '__main__':
    # arguments
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
        description=("Run a server to receive ping and respond " "with pong to compute rtt."),
    )
    parser.add_argument(
        "-l",
        "--logger",
        help='Save all server output in log file.',
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
        "-sd",
        "--simulate_delay",
        help=('Simulate delay in server-side with minimum 10ms and maximum 200ms.'),
        action='store_true',
    )
    parser.add_argument(
        "-sl",
        "--simulate_loss",
        help=('Simulate server-side loss with 25%% of change.'),
        action='store_true',
    )
    args = parser.parse_args()

    # stdout change
    if args.logger:
        previous = sys.stdout
        sys.stdout = open('server_log.txt', 'a', encoding='utf8')

    # server run
    server: Server = UDPServer(int(args.timeout))

    # settings
    if args.simulate_delay:
        server.set_setting('simulate_delay', True)

    if args.simulate_loss:
        server.set_setting('simulate_loss', True)

    server.emmit_setting()
    server.connect('127.0.0.1', 3000)
    server.listen()

    # revert stdout change
    if args.logger:
        sys.stdout.close()
        sys.stdout = previous
