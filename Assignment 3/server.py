from socket import *
import struct
import os

directory = "./server_dir" # Directory where image store
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM) # Create a UDP socket
serverSocket.bind(('',serverPort)) # Assign IP address and port number to socket   
print('The server is ready to receive')
while True:
    packet_recv, clientAddress = serverSocket.recvfrom(1032) 
    # Receive the filename_bytes from the client that client want to get

    # slicing the packet to get the header(first 8 bytes) and the filename(ramaining bytes)
    header_recv = packet_recv[:8] 
    filename_bytes = packet_recv[8:]
    # receive the seq # and ack # of from client
    seq_recv, ack_recv = struct.unpack("!II", header_recv)
    # Receive the clientAddress
    seq_send = 0 # the seq # we will send to client next time 
    ack_send = 0 + (len(filename_bytes) - 1) + 1 # the ack current ack # of server
    if filename_bytes is not None:
        filename = filename_bytes.decode() # decode filename_bytes as filename
        filepath = os.path.join(directory, filename) # the path we want to find the file
        with open(filepath, "rb") as file:
            # "rb": read in binary
            file_data = file.read() # read file into file_data
        for i in range(0, len(file_data), 1024):
            if i + 1023 > len(file_data):
                payload_send = file_data[i:]
            else:
                payload_send = file_data[i: i + 1024]
            header_send = struct.pack("!II", seq_send, ack_send)
            packet_send = header_send + payload_send
            serverSocket.sendto(packet_send, clientAddress)
            seq_send += len(payload_send)