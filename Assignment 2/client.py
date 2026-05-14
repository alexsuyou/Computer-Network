from socket import *
import struct
import os

# Definate a function to receive all data
def recv_all(count): # count: the length of the file which was sent  
    data = b""
    while len(data) < count:
        remaining = count - len(data)
        data_chunk = clientSocket.recv(min(remaining, 4096)) # In case data_chunk get data from next packet
        
        if not data_chunk:# if the connection disrupt accidentally

            return None
        data += data_chunk
    return data

directory = "./client_dir" # Directory where we store the image from server
serverName = '127.0.0.1' # server name is local host
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
clientSocket.connect((serverName, serverPort)) # Connect to the server
while True:
    user_input = input().split(" ") # Get user input
    if user_input[0] == "ls":
        # Packing the header
        # !: Use network byte order (Big-Endian)
        # H: Magic number (2 bytes)('MF' is ASCII)
        # B: Command Code (1 byte) (0x01 for 'ls')
        # I: Payload Length (4 bytes)
        header_send = struct.pack("!HBI", 0x4D46, 0x01, 0) # Create header
        clientSocket.sendall(header_send) # Send the header to the server
        header_recv = recv_all(7) # Receive the header from the server
        if header_recv: # in case connection interrupt
            magic_number, cmd, length = struct.unpack("!HBI", header_recv) # Unpack the header
            if magic_number == 0x4D46 and cmd == 0x04:
                file_list = recv_all(length) # Get the file list from the server
                if file_list is None:
                    print("Connection Interupt")
                    break
                print(file_list.decode())
    elif user_input[0] == "get":
        filename = user_input[1]
        header_send = struct.pack("!HBI", 0x4D46, 0x02, len(filename.encode()))
        clientSocket.sendall(header_send + filename.encode()) 
        header_recv = recv_all(7)
        if header_recv:  # in case connection interrupt
            magic_number, cmd, length = struct.unpack("!HBI", header_recv)
            if magic_number == 0x4D46:
                if cmd == 0x04:
                    # if the file is exit in server
                    print(f"{filename}is downloading...")
                    filepath_to_save = os.path.join(directory, filename) # The path we want to save the file
                    file_data = recv_all(length)
                    if file_data is None:
                        print("Connection Interupt")
                        break
                    with open(filepath_to_save, "wb") as f: # wb: write in binary
                        f.write(file_data)
                        print(f"{filename} Download Successful!")
                else: # if the file is not exit in server
                    error_msg_data = recv_all(length)
                    if error_msg_data is None:
                        print("Connection Interupt")
                        break
                    print(error_msg_data.decode())
    elif user_input[0] == "quit":
        header_send = struct.pack("!HBI", 0x4D46, 0x03, 0) # Create header
        clientSocket.sendall(header_send)
        print("Connected closed")
        clientSocket.close()
        break
    else:
        print("Error input.")  