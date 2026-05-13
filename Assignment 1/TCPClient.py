from socket import *
serverName = '127.0.0.1' # server name is local host
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
clientSocket.connect((serverName, serverPort)) # Connect to the server
while True:
    sentence = input('Input two numbers separated by a comma (or exit): ') # Get user input
    clientSocket.send(sentence.encode()) # Send the sentence to the server
    if sentence == "exit":
        # Wait for the server to close the connection and send FIN
        data = clientSocket.recv(1024)
        if not data:
            print('Connection closed by the server.')
        clientSocket.close()
        break
    modifiedSentence = clientSocket.recv(1024).decode() # Receive the modified sentence from the server
    print('The multiple of two number is: ', modifiedSentence) # Print the multiple of the two numbers
    