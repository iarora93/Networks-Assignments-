#importing the modules
import socket as soc
import logging as log
import sys

message = {"HELLO":"hello", "WORLD":"world","GOODBYE":"goodbye",
           "FAREWELL":"farewell","EXIT":"exit","OK":"ok"}
machine_ip = '127.0.0.1'

# server_tcp accepts port as the argument
def server_tcp(port):
    try:
        # create server socket
        tcp_server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        log.info("TCP socket created successfuly")
        tcp_server.bind((machine_ip, port))
        tcp_server.listen(1)
        entire=True
        conn=1
        # accept the client connection
        while conn==1:
            client, addr = tcp_server.accept()
            print("Connected with Client : ",  str(addr))

            # receive data from the client and send reply
            while entire:
                msg = client.recv(255)
                rec_str = msg.decode('utf-8')
                print("Client Message: ",rec_str)

                if rec_str == message.get("HELLO"):
                    client.sendall(message.get("WORLD").encode('utf-8'))
                    print("Server Message: ",message.get("WORLD"))
                elif rec_str == message.get("GOODBYE"):
                     client.sendall(message.get("FAREWELL").encode("utf-8"))
                     print("Server Message: ",message.get("FAREWELL"))
                     log.info("Terminating Client socket connection ")
                     client.close()
                     break
                elif rec_str == message.get("EXIT"):
                     client.sendall(message.get("OK").encode("utf-8"))
                     print("Server Message: ", message.get("OK"))
                     entire = False
                     conn = 2
                     client.close()
                     log.info("Terminating Client socket connection")
                     log.info("Terminating server socket connection")
                else:
                     client.sendall(rec_str.encode("utf-8"))
                     print("Server Message: ", rec_str)

    except Exception as err:
        log.info(err)

# client_tcp accepts host and port as the argument
def client_tcp(host,port):
     # create client socket and connect to server and it's port
      tcp_client = soc.socket()
      log.info("TCP socket created successfuly")
      tcp_client.connect((machine_ip,port))
      display_msg = input("Type your Message:")

      # send and receive data from  server
      while True:
           tcp_client.send(display_msg.encode("utf-8"))
           msg = tcp_client.recv(255)
           srv_msg = msg.decode("utf-8")
           print("Server Message:  ",srv_msg)

           if srv_msg == message.get("FAREWELL"):
               log.info("Closing the client connection")
               break
           elif srv_msg == message.get("OK"):
               log.info("Closing the client connection")
               break
           display_msg = input("Type your Message:")

# server_udp fucntion accepts port as teh argument
def server_udp(port):
    try:
        # Create server socket and bind to host and port
        udp_server = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        log.info("UDP socket created successfuly")
        udp_server.bind((machine_ip, port))

        # Receive data frome client and send reply
        while True:
            msg, addr = udp_server.recvfrom(255)
            print("connectd to client ", addr)
            rec_str = msg.decode('utf-8')

            if rec_str == message.get("HELLO"):
                udp_server.sendto(message.get("WORLD").encode('utf-8'), addr)
                print("Client Message: ", rec_str)
                print("Server Message: ", message.get("WORLD"))
            elif rec_str == message.get("GOODBYE"):
                udp_server.sendto(message.get("FAREWELL").encode("utf-8"), addr)
                print("Client Message: ",rec_str)
                print("Server Message: ", message.get("FAREWELL"))

            elif rec_str == message.get("EXIT"):
                udp_server.sendto(message.get("OK").encode("utf-8"), addr)
                print("Client Message: ", rec_str)
                print("Server Message: ", message.get("OK"))
                log.info("Terminating server socket connection")
                break
                #server.close()
            else:
                udp_server.sendto(rec_str.encode("utf-8"), addr)
                print("Client Message: ", rec_str)
                print("Server Message: ", rec_str)

    except Exception as err:
           log.info(err)

# client_udp accepts port as teh argument
def client_udp(port):
    try:
       # create a client socket
       udp_client = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
       log.info("UDP socket created successfuly")
       display_msg = input("Type your Message:")

       # send and receive data from server
       while True:
           udp_client.sendto(display_msg.encode("utf-8"), (machine_ip, port))
           msg, addr = udp_client.recvfrom(255)
           rcv_msg = msg.decode("utf-8")
           print("Server Message: ",rcv_msg)

           if rcv_msg == message.get("OK"):
              break

           if rcv_msg == message.get("FAREWELL"):
              log.info("Closing the client connection")
              udp_client.close()
              break

           display_msg = input("Type your Message:")
    except Exception as err:
       log.info(err)
