from socket import *
import struct
import os

directory = "./server_dir" # Directory where image store
N = 4 # slicing window size
N_bytes = N * 1024 # slicing window bytes size
T = 0.5 # timeout interval
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM) # Create a UDP socket
serverSocket.bind(('',serverPort)) # Assign IP address and port number to socket   

print('[System] The server is ready to receive')

while True:
    packet_recv, clientAddress = serverSocket.recvfrom(1032) 
    # Receive the filename_bytes from the client that client want to get

    # slicing the packet to get the header(first 8 bytes) and the filename(ramaining bytes)
    header_recv = packet_recv[:8] 
    payload_recv = packet_recv[8:]
    # receive the seq # and ack # of from client
    seq_recv, ack_recv = struct.unpack("!II", header_recv)
    # Receive the clientAddress
    seq_send = ack_recv # the seq # we will send to client next time 
    ack_send = 0 + (len(payload_recv) - 1) + 1 # the ack current ack # of server
    if payload_recv is not None:
        filename = payload_recv.decode() # decode filename_bytes as filename
        filepath = os.path.join(directory, filename) # the path we want to find the file
        with open(filepath, "rb") as file:
            # "rb": read in binary
            file_data = file.read() # read file into file_data
        # for i in range(0, len(file_data), 1024):
        next_seq = seq_send # initial next_seq as the first seq # server will send
        base = 0 # The base of the sliding window (oldest unacknowledged byte)
        serverSocket.settimeout(T) # set the timeout interval before sending packet
        while base < len(file_data):
            while seq_send < base + N_bytes and seq_send < len(file_data):
                if seq_send + 1023 > len(file_data):
                    payload_send = file_data[seq_send:]
                else:
                    payload_send = file_data[seq_send:seq_send + 1024]
                header_send = struct.pack("!II", seq_send, ack_send)
                packet_send = header_send + payload_send
                serverSocket.sendto(packet_send, clientAddress)
                seq_send += len(payload_send)
            try:
                packet_recv, clientAddress = serverSocket.recvfrom(1032)
                header_recv = packet_recv[:8]
                seq_recv, ack_recv = struct.unpack("!II", header_recv)
                if ack_recv > base:
                    base = ack_recv
            except timeout:
                print(f"[TIMEOUT] Timer expired (T={T}s)! Retransmitting window burst from Base: {base}")
                seq_send = base
        
        # Send an empty packet (0-byte payload) to notify the client that the file transfer is complete
        header_send = struct.pack("!II", seq_send, ack_send) 
        serverSocket.sendto(header_send, clientAddress)
        
        # Receive the last packet transfer from client
        try:
            serverSocket.recvfrom(1032) 
            print("[System] Successfully received the final ACK. Buffer cleared!")
        except timeout:
            # timeout occurs
            # Final ACK missed but transfer is complete.
            # Retransmission unnecessary; this prevents server crash.
            print("[System] Final ACK timed out or lost, but the transfer is already complete")
            print("[System] There is unnecessary to retransfer the end packet again")
        
        serverSocket.settimeout(None) # clear the timeout interval after finish sending packet
