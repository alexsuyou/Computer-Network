from socket import *
import struct
import os

directory = "./client_dir" # Directory where we store the image from server
serverName = '127.0.0.1' # server name is local host
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # Create a UDP socket
clientSocket.connect((serverName, serverPort)) # Connect to the server
while True:
    filename = input('Which of file you want to save?') # Get user input
    clientSocket.sendto(filename.encode(),(serverName, serverPort))
    file, serverAddress = clientSocket.recvfrom(1024)
    clientSocket.close()
        