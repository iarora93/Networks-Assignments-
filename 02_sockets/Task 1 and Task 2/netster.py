import os
import time
import argparse
import socket
import logging as log

# Importing the assignment module a2.
from a2 import *

DEFAULT_PORT=12345

# This Server fucntion accepts host, protocol and port as the argument
# host is the Server IP, protocl is UDP/TCP and port is the Default port 12345'''
def run_server(host, port, protocol):
    log.info("Hello, I am a server...!!")

    if protocol is True:
        server_udp(port)
    else:
         server_tcp(port)

# This Client fucntion accepts host and port as the argument
# host is the Server IP and port is the Default port 12345'''
def run_client(host, port, protocol):
    log.info("Hello, I am a client...!!")

    if protocol is True:
        client_udp(port)
    else:
         client_tcp(host,port)

def main():
    parser = argparse.ArgumentParser(description="SICE Network netster")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                        help='listen on/connect to port <port> (default={}'
                        .format(DEFAULT_PORT))
    parser.add_argument('-i', '--iface', type=str, default='0.0.0.0',
                        help='listen on interface <dev>')
    parser.add_argument('-u', '--udp', action='store_true',
                        help='use UDP (default TCP)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Produce verbose output')
    parser.add_argument('host', metavar='host', type=str, nargs='?',
                        help='connect to server at <host>')

    args = parser.parse_args()
    print(args)
    # configure logging level based on verbose arg
    level = log.DEBUG if args.verbose else log.INFO

    # Here we determine if we are a client or a server depending
    # on the presence of a "host" argument.
    if args.host:
        log.basicConfig(format='%(levelname)s:client: %(message)s',
                        level=level)
        run_client(args.host, args.port, args.udp)
        print(args.udp)
    else:
        log.basicConfig(format='%(levelname)s:server: %(message)s',
                        level=level)
        run_server(args.host, args.port, args.udp)

if __name__ == "__main__":
    main()

