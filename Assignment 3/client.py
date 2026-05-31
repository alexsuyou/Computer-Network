from socket import *
import struct
import os
import random # for determining if packet loss occurred

directory = "./client_dir" # Directory where we store the image from server
serverName = '127.0.0.1' # server name is local host
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # Create a UDP socket
clientSocket.connect((serverName, serverPort)) # Connect to the server
save_another_bool = True
while save_another_bool:
    
    filename = input('Which of file you want to save? ') # Get user input

    seq_send = 0 # initial seq #
    ack_send = 0 # initial ack #

    header_send = struct.pack("!II", seq_send, ack_send)
    # !: Use network byte order
    # I(first): Seq Number (4 bytes)
    # I(second): Ack Number (4 bytes)
    
    packet_send = header_send + filename.encode()
    clientSocket.sendto(packet_send, (serverName, serverPort)) # send the packet to server
    

    filepath = os.path.join(directory, filename)
    expected_seq = ack_send
    print(f"{filename} is downloading...")
    with open(filepath, "wb") as file: # open the file before checking is there any loss packet
        while True:
            loss_prob = random.random() # get a random num to simulate the loss probability

            packet_recv, serverAddress = clientSocket.recvfrom(1032)
            # packet_recv: the file packet receive from server
            # serverAddress: get the server address
            header_recv = packet_recv[:8]
            payload_recv = packet_recv[8:]
            seq_recv, ack_recv = struct.unpack("!II", header_recv)
            
            if loss_prob < 0.15:
                print(f"[Packet Loss] Ignored Seq: {seq_recv}, Length: {len(payload_recv)} bytes")
                continue
            else:
                if seq_recv == ack_send:
                    ack_send += len(payload_recv)
                    if len(payload_recv) == 0:
                        header_send = struct.pack("!II", seq_send, ack_send)
                        packet_send = header_send
                        clientSocket.sendto(packet_send, serverAddress)
                        break
                    else:
                        file.write(payload_recv)

                header_send = struct.pack("!II", seq_send, ack_send)
                packet_send = header_send
                clientSocket.sendto(packet_send, serverAddress)
    print(f"{filename} Download Successful!")
    print()
    save_another = input("Do you want to save another file?(Please enter \"yes\"(\"y\") or \"no\"(\"n\") ").lower()
    if save_another == "no" or save_another == "n":
        save_another_bool = False
        clientSocket.close()
        print("[System] Socket closed. Client terminated.")
        