'''*************************************************************
  netster SOURCE FILE - Nischith Nanjundaswamy (ncnanjun)
  CREATED: 09/22/2018
  This is an Networks assignments
  This code provide Server and Client socket functionality
*************************************************************'''

import os
import time
import argparse
import socket
import logging as log

# Importing the assignment module a2.
from a3 import *


DEFAULT_PORT=2196

# This Server fucntion accepts host, protocol and port as the argument
# host is the Server IP, protocl is UDP/TCP and port is the Default port 12345'''
def run_server( port, f, file,rudp):
    log.info("Hello, I am a server...!!")
    port = int(port);
    #print("PORT",port);
    if rudp == 1:
        print("Task 2")
        print(port,f)
        server2(port, f)
    elif rudp==2:
        print("Task 3 &4")
        server3(port, f)


# This Client fucntion accepts host and port as the argument
# host is the Server IP and port is the Default port 12345'''
def run_client(host, port,rudp, f):
    log.info("Hello, I am a client...!!")
    port = int(port);
    print(host, port,rudp, f)
    if rudp==1:
        #print(r)
        print("Task 2")
        #udp_server_socket_2(
        client2(port, f)

    elif rudp==2:
        print("Task 3 &4")
        client3(port, f)


    #udp_client_socket(port,f)

def main():
    parser = argparse.ArgumentParser(description="SICE Network netster")
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT,
                        help='listen on/connect to port <port> (default={}'
                        .format(DEFAULT_PORT))
    parser.add_argument('-i', '--iface', type=str, default='0.0.0.0',
                        help='listen on interface <dev>')
    parser.add_argument('-f', '--file', type=str,
                        help='file to read/write')
    parser.add_argument('-u', '--udp', action='store_true',
                        help='use UDP (default TCP)')
    parser.add_argument('-r', '--rudp', type=int, default=0,
                        help='use RUDP (1=stopwait, 2=gobackN)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Produce verbose output')
    parser.add_argument('host', metavar='host', type=str, nargs='?',
                        help='connect to server at <host>')

    args = parser.parse_args()
    print(args)
    # configure logging level based on verbose arg
    level = log.DEBUG if args.verbose else log.INFO

    f = None

     # open the file if specified
    if args.file:
        try:
            mode = "rb" if args.host else "wb"
            f = open(args.file, mode)
        except Exception as e:
            print("Could not open file: {}".format(e))
            exit(1)

    # Here we determine if we are a client or a server depending
    # on the presence of a "host" argument.
    if args.host:
        log.basicConfig(format='%(levelname)s:client: %(message)s',
                        level=level)
       # run_client(args.host, args.port,args.rudp , f)
        run_client(args.host, args.port,args.rudp, f)
        print(args.host, args.port,args.rudp, f)
    else:
        log.basicConfig(format='%(levelname)s:server: %(message)s',
                        level=level)
        run_server(args.port,f, args.file,args.rudp)

if __name__ == "__main__":
    main()
