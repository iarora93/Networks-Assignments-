import socket
import threading



import logging as log

msglist = {"HELLO":"hello", "WORLD":"world","GOODBYE":"goodbye",
           "FAREWELL":"farewell","EXIT":"exit","OK":"ok"}
machine_ip = '127.0.0.1'
entire=True
conn=1


def server_tcp(tcp_client,tcp_server,addr):
    log.info("Thread started")
    global entire,conn
    while entire:
        msg = tcp_client.recv(255)
        msg_client = msg.decode('utf-8')
        print("Client Message: ",msg_client)
        if msg_client == msglist.get("HELLO"):
                    tcp_client.sendall(msglist.get("WORLD").encode('utf-8'))
                    print("Server Response: ",msglist.get("WORLD"))
        elif msg_client == msglist.get("GOODBYE"):
                     tcp_client.sendall(msglist.get("FAREWELL").encode("utf-8"))
                     print("Server Response: ",msglist.get("FAREWELL"))
                     log.info("Terminating Client  connection ")
                     tcp_client.close()
                     break
        elif msg_client == msglist.get("EXIT"):
            conn=0
            tcp_client.sendall(msglist.get("OK").encode("utf-8"))
            print("Server Response: ", msglist.get("OK"))
            log.info("Terminating Client  connection")
            tcp_client.close()
            tcp_server.close()
            entire=False
            log.info("Terminating server  connection")
            return
        else:
            tcp_client.sendall(msg_client.encode("utf-8"))
            print("Server Response: ", msg_client)
    return

#listens for clients and accepts and handles client and starts its own thread
def tcp_server_thread(port):
    global conn
    try:
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info("trying to connect....")
        tcp_server.bind((machine_ip, port))
        log.info("TCP Socket connected Successfully")
        tcp_server.listen(2)
        tcp_server.settimeout(1)
        while 1:
            try:
                if conn==0:
                    tcp_server.close()
                    print("Server Disconnected can not make any more client connections")
                    return
                tcp_client, addr = tcp_server.accept()
                print("Connected with Client : ", addr)
                thread = threading.Thread(target = server_tcp,args=(tcp_client,tcp_server,addr))
                thread.start()
            except :
                pass

    except Exception as err:
        log.info(err)

#starts a client connection with the server and receives responses.
#Immediately checks if able to make connection with server

def client_tcp(machine_ip,port):
      global conn
      if conn==0:
        print("Not Accepting more connections")
        return
      try:
        tcp_client = socket.socket()
        log.info("Trying to connect")
        tcp_client.connect((machine_ip,port))
        log.info("TCP socket created successfuly")
        display_msg  = input("Client Message:")
        while True:
           tcp_client.send(display_msg .encode("utf-8"))
           msg = tcp_client.recv(255)
           srv_msg = msg.decode("utf-8")
           print("Server Message:  ",srv_msg)
           if srv_msg == msglist.get("FAREWELL"):
               log.info("Closing the client connection")
               break
           elif srv_msg == msglist.get("OK"):
               tcp_client.close()
               log.info("Closing the client connection")
               break
           display_msg  = input("Client Message:")
      except:
        print("Server issue not able to Connect")

def server_udp(udp_server,msg,addr):
    global entire,conn

    try:
            msg_client = msg.decode()
            #print(msg_client)
            print("Client Message: ", msg_client)
            if msg_client == msglist.get("HELLO"):
                response = str.encode("world")
                udp_server.sendto(response, addr)
                print("Server Response: world")
            elif msg_client == msglist.get("GOODBYE"):
                response = str.encode("farewell")
                udp_server.sendto(response, addr)
                print("Server Response: farewell")
                print("Client Connection Closed")
            elif msg_client == msglist.get("EXIT"):
                conn=0
                #entire=False
                response = str.encode("ok")
                udp_server.sendto(response, addr)
                print("Server Response: ok")
                print("Client Connection Closed")
                print("Terminating Connection: Server Closed")
                return
            elif msg_client:
                udp_server.sendto(msg, addr)
                print("Server Response:", msg_client)
    except:
            pass

#listens for clients and accepts and handles client and starts its own thread
def udp_server_thread(PORT):
    global conn

    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP Socket creating connection")
    server_address = (machine_ip, PORT)
    print("Starting the UDP server on:", server_address)
    udp_server.bind(server_address)
    if conn==0:
            udp_server.close()
            print("Server Disconnected can not make any more client connections")
            return
    print("Waiting for a new client")
    udp_server.settimeout(1)
    while True:
        try:
            if conn==0:
                udp_server.close()
                print("Server Disconnected can not make any more client connections")
                return
            msg, addr = udp_server.recvfrom(255)
            print("Connected with Client : ", addr)
            thread=threading.Thread(target=server_udp,args=(udp_server,msg,addr),daemon=True)
            thread.start()
        except:
            pass

#starts a client connection with the server and receives responses.
#if no response from the server within 3 seconds then Server is down
def client_udp(HOST,PORT):
    global conn
    if conn==0:
        print("Not Accepting more connections")
        return
    log.info("Trying to connect")
    udp_client  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (HOST,PORT)
    udp_client.settimeout(2)
    log.info("UDP socket created successfuly")
    try:
        while True:
            display_msg = input("Client Message:")
            udp_client.sendto(display_msg.encode("utf-8"), (machine_ip, PORT))
            msg, addr = udp_client.recvfrom(255)
            rcv_msg = msg.decode("utf-8")
            print("Server Message:", rcv_msg)
            if rcv_msg== msglist.get("OK"):
                log.info("Closing the client connection due to exit")
                udp_client.close()
                break
            if rcv_msg== msglist.get("FAREWELL"):
                log.info("Closing the client connection due to goodbye")
                udp_client.close()
                break
    except:
        print("Server issue not able to Connect")

