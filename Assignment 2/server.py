from socket import *
import struct
import os

# Definate a function to receive all data
def recv_all(count): # count: the length of the file which was sent  
    data = b""
    while len(data) < count:
        remaining = count - len(data)
        data_chunk = connectionSocket.recv(min(remaining, 4096)) # In case data_chunk get data from next packet
        
        if not data_chunk:# if the connection disrupt accidentally

            return None
        data += data_chunk
    return data

directory = "./server_dir" # Directory where image store
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) # Create a TCP wellcoming socket
serverSocket.bind(('',serverPort)) # Assign IP address and port number to socket   
serverSocket.listen(1) # Listen for TCP connections
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept() # Accept TCP connection from the client
    while True:
        header_recv = recv_all(7) # Receive the header from the client
        if header_recv :
            magic_number, cmd, length = struct.unpack("!HBI", header_recv) # Unpack the header
            if magic_number == 0x4D46: # Check the magic number
                if cmd == 0x01: # command is "ls"
                    file_list = os.listdir(directory) # Get the list of the file in the directory
                    file_list_str = "\n".join(file_list) # Create a string of the file list
                    header_send = struct.pack("!HBI", 0x4D46, 0x04, len(file_list_str.encode())) # Create header
                    connectionSocket.sendall(header_send + file_list_str.encode())
                elif cmd == 0x02: # command is "get"
                    filename_bytes = recv_all(length) # Receive the filename_bytes from the client that client want to get
                    if filename_bytes is not None:
                        filename = filename_bytes.decode() # decode filename_bytes as filename
                        filepath = os.path.join(directory, filename)
                        with open(filepath, "rb") as file: # "rb": read in binary
                            file_data = file.read() # read file into file_data
                        header_send = struct.pack("!HBI", 0x4D46, 0x04, len(file_data))
                        connectionSocket.sendall(header_send + file_data)
                elif cmd == 0x03:
                    connectionSocket.close()
                    break