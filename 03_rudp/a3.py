
#importing the modules
import socket
import logging as log
import sys
import time
import threading

message = {"HELLO":"hello", "WORLD":"world","GOODBYE":"goodbye",
           "FAREWELL":"farewell","EXIT":"exit","OK":"ok"}
HOST_IP = '10.10.2.10'
#HOST_IP = '127.0.0.1'
ACK_Window = 100


#This function is used for implementing  alternating bit, stop-and-wait protocol
# accepts port as the argument
def server2(port,f):
    try:
        # Create server socket and bind to host and port
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        log.info("UDP socket created successfuly \n")
        server.bind((HOST_IP, port))
        msg_details={}
        ack_count = None
        # Receive data frome client and send reply
        while True:
            data, addr = server.recvfrom(2000)
            #print("connectd to client ", addr, "\n")
            client_message = data.decode('utf-8','ignore')
            if client_message == message.get("GOODBYE"):
                  server.sendto(message.get("FAREWELL").encode("utf-8"), addr)
                  print("Message from client: ",client_message)
                  print("Server Message: ", message.get("FAREWELL"))
                  f.close()
                  break
            else:
                 msg_details = client_message.split('&&')
                 print("Message Sequence number received :- ",msg_details[0] )
                 print("Message length received :- ",msg_details[1])
                 message_write = msg_details[2]
                 ACK = msg_details[0]
                 if msg_details[0] == '0' and ack_count!= msg_details[0]:
                    server.sendto(('0').encode("utf-8"),addr)
                    print("sending ACK-0 to client")
                    f.write(message_write.encode('utf-8'))
                 elif msg_details[0] == '0' and ack_count == msg_details[0]:
                     server.sendto(('0').encode("utf-8"), addr)
                     print("Duplicate packet received.Discarding the packet and sending ack")
                     print("Sending ACK-0 to client")
                 elif msg_details[0] == '1' and ack_count!= msg_details[0]:
                         server.sendto(('1').encode("utf-8"), addr)
                         print("sending ACK-1 to client")
                         f.write(message_write.encode('utf-8'))
                 else:
                     server.sendto(('1').encode("utf-8"), addr)
                     print("Duplicate packet received. Discarding the packet and sending ack")
                     print("sending ACK-1 to client")
                 ack_count = ACK
    except Exception as err:
           log.info(err)



#This function is used for implementing  alternating bit, stop-and-wait protocol
# accepts port as the argument
# send packets with sequence number 0 or 1 and start timer.
# default value of timer is set to 100 miliseconds
def client2(port,f):
    try:
       len_message = 0
       seq_no = 0

       # create a client socket
       client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       log.info("UDP socket created successfully")

       # Read line of data from the file and send it to server.
       # seq_no is the sequence number 0/1
       # len_message is the lenth of message
       for line in f:
               message = line.decode('utf-8','ignore')
               len_message = len(line)
               header = str(seq_no) +'&&'+str(len_message)
               rudp_message = header +'&&'+ message
               print("Sending Rudp message with seq_no:- ", seq_no)
               client.sendto(rudp_message.encode('utf-8'), (HOST_IP, port))
               client_msg_time = int(round(time.time() * 1000))

               server_ack_received = None
               server_ack_received = ACK_time(client, client_msg_time)

               while server_ack_received == None:
                   print(" ACK not received from Server. "
                         "Resending the data with seq_no:- ", seq_no )
                   client.sendto(rudp_message.encode('utf-8'), (HOST_IP, port))

                   client_msg_time = int(round(time.time() * 1000))
                   server_ack_received = ACK_time(client, client_msg_time)

               while server_ack_received.decode('utf-8') != str(seq_no):
                   print("Received acknowledgement ACK:- ",server_ack_received.decode('utf-8'),
                         "is not matching seq_no:- ", seq_no,'\n')
                   print("Duplicate ACK received.Discarding the ACK and "
                         "Resending the data and wait until proper "
                         "ACK received for data with Seq number ",str(seq_no))
                   client.sendto(rudp_message.encode('utf-8'), (HOST_IP, port))
                   client_msg_time = int(round(time.time() * 1000))
                   server_ack_received = ACK_time(client, client_msg_time)

               if server_ack_received.decode('utf-8') == str(seq_no):
                       print("Received acknowledgement ACK:- ", server_ack_received,
                         "is matching seq_no:- ", seq_no)

               if server_ack_received.decode('utf-8') == str(0):
                   seq_no = 1
               else:
                   seq_no = 0

       # send and receive data from server
       print("Enter goodbye to exit client")
       send_str = input("Send >>")
       while True:
           client.sendto(send_str.encode("utf-8"), (HOST_IP, port))
           data3, addr = client.recvfrom(255)
           server_reply = data3.decode("utf-8")
           print("Message from Server: ",server_reply)
           if server_reply == message.get("FAREWELL"):
              log.info("Closing the client connection")
              client.close()
              break
           send_str = input("Send >>")
    except Exception as err:
       log.info(err)




#This function is used for implementing  alternating bit, stop-and-wait protocol
# function to receive acknowledgement.
# accepts message sent time and client socket as parameters
#This helps you to set an Acknowledge time window during which we should receive a reply
def ACK_time(client,client_msg_time):
    start = int(round(time.time() * 1000))
    passed = start - client_msg_time
    while(passed < ACK_Window):
        client.setblocking(False)
        try:
           data = client.recv(2000)
           #print("Data in Client socket =  ",data)
           if data != None:
               return data
        except socket.error:
           pass
        start = int(round(time.time() * 1000))
        passed = start - client_msg_time
    return None





# This function is used for implementing  go-back-N protocol and Congestion control
#importing the modules
HOST_IP = '10.10.2.10'
#HOST_IP = '127.0.0.1'
client_seq_no = 0
server_seq_no = None
ack_no = None
client_msg_time = None
window_size = 4

# udp server socket fucntion
# accepts port as the argument
def server3(port,f):
    try:
        # Create server socket and bind to host and port
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        log.info("UDP socket created successfuly")
        server.bind((HOST_IP, port))

        # Receive data frome client and send reply
        while True:
            data, addr = server.recvfrom(5000)
            #print("connectd to client ", addr)
            client_message = data.decode('utf-8')

            if client_message == message.get("GOODBYE"):
                server.sendto(message.get("FAREWELL").encode("utf-8"), addr)
                print("Message from client: ",client_message)
                print("Send reply >> ", message.get("FAREWELL"))
                f.close()
                #time.sleep(2)
                break
            else:
                msg_details = client_message.split('&&')
                print("Message Sequence number received :-", msg_details[0])
                print("Message length received :- ", msg_details[1])
                message_write = msg_details[2]
                #print ("encoding:132")

                ACK = msg_details[0]
                if msg_details[0] == '0':
                    #print("encoding:138")
                    server.sendto(('0').encode("utf-8"), addr)
                    print("sending ACK-0 to client")
                    f.write(message_write.encode('utf-8'))
                    ack_count = msg_details[0]
                elif (int(ack_count) + 1) == int(ACK):
                   #print("encoding:143")
                    server.sendto(ACK.encode("utf-8"), addr)
                    print("sending ACK-", ACK.encode("utf-8"), "to client")
                    f.write(message_write.encode('utf-8'))
                    ack_count = int(ACK)
                else:
                    #print("encoding:148")
                    server.sendto(str(ack_count).encode(("utf-8")), addr)
                    print("Received packet with sequence number",ACK ,"is not in order")
                    print("Did not receive packet with seq nuber",(int(ack_count) + 1),
                          "sending ACK-",ack_count ,"to client")

    except Exception as err:
        log.info(err)


# udp client socket function
# accepts port as the argument
def client3(port,f):
    # create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    log.info("UDP socket created successfully")
    len_message = 0
    client_file_message = []

    for line in f:
        client_file_message.append(line.decode('utf-8', 'ignore'))
    length = len(client_file_message)

    thread1 = None
    thread2 = None
    print("Creating thread1 and thread2 for "
          "sending data packets and receiving acknowldgements")
    try:
        thread1 = threading.Thread(target=send_ack, args=(client,length,client_file_message,port))
        thread1.start()
    except:
        print("Closing  connection")
    try:
        thread2 = threading.Thread(target=receive_ack, args=(client,length))
        thread2.start()
    except:
        print("Closing  connection")

    thread1.join()
    thread2.join()
    print ("Exited both the threads")

    while True:
        try:
            data, addr = client.recvfrom(255)
        except socket.error:
            break
        rcv_message = data.decode("utf-8")
        print("In while after thread ",rcv_message)
        if rcv_message == None:
            break

    print("Enter goodbye to exit client")
    send_str = input("Send >>")

    while True:
        client.sendto(send_str.encode("utf-8"), (HOST_IP, port))
        client.setblocking(True);
        try:
            data, addr = client.recvfrom(255)
        except socket.error:
            pass
        rcv_message = data.decode("utf-8")
        print("Message from Server: ",rcv_message)

        if rcv_message == message.get("FAREWELL"):
           log.info("Closing the client connection")
           client.close()
           break

        send_str = input("Send >>")


# function to send data packets.
# delay introduced by default is 75 milisecond
# default port is 2196.
# congestion window window_size is set to 4 and doubles every time.
# when there is a packet loss congestion window is reduced to half.
def send_ack(client,length,client_file_message,port):
    global client_seq_no, server_seq_no, client_msg_time, window_size
    while client_seq_no < length:
        flag = True
        if window_size == 0:
            window_size = 1
        for i in range(window_size):
            if client_seq_no + i < length:
                data_packets(client_file_message[client_seq_no + i], client_seq_no + i, client, port)
                if i == 0:
                    client_msg_time = int(round(time.time() * 1000))
            else:
                client_seq_no = length
                sys.exit();
                break
        while (client_msg_time + 75) > int(round(time.time() * 1000)):
            if server_seq_no == (client_seq_no + window_size):
                flag = False
                window_size *= 2
                break
            continue
        if flag:
            window_size /= 2
            window_size = int(window_size)
        client_seq_no = server_seq_no
    sys.exit();

# function to send data packets.
# accept client socket, port, actual data from file and sequence number
def data_packets(message, client_seq_no, client, port):
    len_message = len(message)
    header = str(client_seq_no) + '&&' + str(len_message)
    rudp_message = header + '&&' + message
    print("Sending Rudp message with seq_no:- ",client_seq_no, "\n")
    client.sendto(rudp_message.encode('utf-8'), (HOST_IP, port))

# function to receive acknowledgements
# accepts length(number of client_file_message) of the data and client socket
def receive_ack(client,length):
    global server_seq_no, client_msg_time, client_seq_no
    server_ack = None
    server_seq_no = 0

    while server_seq_no < length:
        client.setblocking(False)
        try:
            server_ack = client.recv(2000)
            print("Received ACK from Server",server_ack)
            client_seq_no=int(server_ack)
        except socket.error:
            pass
        if server_ack == None:
            server_ack = '-1'
        if int(server_ack) == server_seq_no:
            server_seq_no = server_seq_no + 1
            print("server_seq_no: ", server_seq_no)
            client_msg_time = int(round(time.time() * 1000))
    sys.exit();


