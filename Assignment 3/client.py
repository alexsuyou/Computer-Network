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
    header_send = struct.pack("!II", 0, 0)
    # !: Use network byte order
    # I(first): Seq Number (4 bytes)
    # I(second): Ack Number (4 bytes)
    
    packet_send = header_send + filename.encode()
    clientSocket.sendto(packet_send, (serverName, serverPort)) # send the packet to server
    file_data, serverAddress = clientSocket.recvfrom(1024)
    # file_data: the file data receive from server
    # serverAddress: get the server address

    filepath = os.path.join(directory, filename)
    with open(filepath, "wb") as file:
        file.write(file_data)
        break
clientSocket.close()
        