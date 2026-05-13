from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) # Create a TCP wellcoming socket
serverSocket.bind(('',serverPort)) # Assign IP address and port number to socket   
serverSocket.listen(1) # Listen for TCP connections
print('The server is ready to receive')
while True:
    connctionSocket, addr = serverSocket.accept() # Accept TCP connection from the client
    while True:
        sentence = connctionSocket.recv(1024).decode() # Receive the sentence from the client
        if not sentence:  # Client closed connection
            break
        if sentence == "exit":
            connctionSocket.close() # Close the connection and send FIN to the client
            break
        num = sentence.split(",")
        result = int(num[0]) * int(num[1]) # Calculate the multiple of the two numbers
        connctionSocket.send(str(result).encode()) # Send the result back to the client
        