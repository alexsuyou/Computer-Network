from socket import *
import struct
import os

directory = "./server_dir" # Directory where image store
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM) # Create a UDP socket
serverSocket.bind(('',serverPort)) # Assign IP address and port number to socket   
print('The server is ready to receive')
while True:
    filename, clientAddress = serverSocket.recvfrom(1024)
    modifiedMessage = filename.decode()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)       