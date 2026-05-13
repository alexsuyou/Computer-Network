from socket import *
import struct
import os

directory = "./server_dir" # Directory where image store


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) # Create a TCP wellcoming socket
serverSocket.bind(('',serverPort)) # Assign IP address and port number to socket   
serverSocket.listen(1) # Listen for TCP connections
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept() # Accept TCP connection from the client
    while True:
        header_recv = connectionSocket.recv(7) # Receive the header from the client
        magic_number, cmd, length = struct.unpack("!HBI", header_recv) # Unpack the header
        if magic_number == 0x4D46: # Check the magic number
            if cmd == 0x01: # command is "ls"
                file_list = os.listdir(directory) # Get the list of the file in the directory
                file_list_str = "\n".join(file_list) # Create a string of the file list
                header_send = struct.pack("!HBI", 0x4D46, 0x04, len(file_list_str.encode())) # Create header
                connectionSocket.send(header_send + file_list_str.encode())
            elif cmd == 0x02: # command is "get"
                filename = connectionSocket.recv(length.decode()) # Receive the filename from the client that client want to get
                filepath = os.path.join(directory, filename)
                with(filepath, "rb") as file: # "rb": read in binary
                    file_data = file.read() # read file into file_data
                header_send = struct.pack("!HBI", 0x4D46, 0x04, len(file_data.encode()))
                connectionSocket.send(header_send + file_data.encode())
               

        if not sentence:  # Client closed connection
            break
        if sentence == "exit":
            connctionSocket.close() # Close the connection and send FIN to the client
            break
        num = sentence.split(",")
        result = int(num[0]) * int(num[1]) # Calculate the multiple of the two numbers
        connctionSocket.send(str(result).encode()) # Send the result back to the client
        