from socket import *
import struct

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
        clientSocket.send(header_send) # Send the header to the server
    elif user_input[0] == "get":
        filename = user_input[1]
        header_send = struct.pack("!HBI", 0x4D46, 0x02, len(filename.encode()))
        clientSocket.send(header_send + filename.encode()) # Send the header and filename to the server

    if sentence == "exit":
        # Wait for the server to close the connection and send FIN
        data = clientSocket.recv(1024)
        if not data:
            print('Connection closed by the server.')
        clientSocket.close()
        break
    modifiedSentence = clientSocket.recv(1024).decode() # Receive the modified sentence from the server
    print('The multiple of two number is: ', modifiedSentence) # Print the multiple of the two numbers
    