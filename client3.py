#####################################################################
# Test client - client3.py                                          #
#                                                                   #
#####################################################################
"""
This simple script simulates a variable number of clients making
requests to the server running at localhost (your computer), port 8888.
Run it by typing:
python client3.py --max-clients=300 --max-conns=1
(You can specify the number of clients/connections-per-client
from the command line.)
Be sure that the server is running before running this script.
"""
# the module argparse is used to make a program accept named command
# line arguments, like --max-clients
import argparse
import errno
import os
import socket


SERVER_ADDRESS = 'localhost', 8888
REQUEST = b"""\
GET /hello HTTP/1.1
Host: localhost:8888

"""

# when this is called, it creates max_clients sockets, simulating
# an equal amount of clients connecting to the server, and sends
# a simple get request (see text above). Each client sends max_conns
# equal requests. The total load that the server will receive will be
# therefore max_clients*max_conns.
def main(max_clients, max_conns):
    socks = []
    for client_num in range(max_clients):
        pid = os.fork()
        if pid == 0:
            for connection_num in range(max_conns):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(SERVER_ADDRESS)
                sock.sendall(REQUEST)
                socks.append(sock)
                print(connection_num)
                os._exit(0)

# read parameters from command line, and call main()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test client for LSBAWS.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--max-conns',
        type=int,
        default=1024,
        help='Maximum number of connections per client.'
    )
    parser.add_argument(
        '--max-clients',
        type=int,
        default=1,
        help='Maximum number of clients.'
    )
    args = parser.parse_args()
    main(args.max_clients, args.max_conns)
