import time
import sys
import random
import os
import filecmp
from socket import *

def send_packet(data, seq_num):     #Sends a packet containing message data and sequence number from client to server
    packet = str.encode(data.decode() + str(seq_num))
    client_socket.sendto(packet, socket_address)

client_socket = socket(AF_INET, SOCK_DGRAM) #Creates UDP socket  
client_socket.settimeout(1)                 #Waits 1 second for reply before timing out

host_ip_address = sys.argv[1]   #Accepts IP Address as input
port_number = 9093              #Fixed port number
socket_address = (host_ip_address, port_number)

input_file = open('inputfile.txt', 'rb')

seq_num = 0     #Starting sequence number
ack = 1         #Starting access number

end_found = False   
start_time = time.time()
while not end_found:
    data = input_file.read(512)     #Reads 512 bytes at a time
    
    retransmission_count = 0        #Keeps track of how many times the message has been retransmitted
    for i in range(6):              #Try 6 times to send packet to server
        send_packet(data, seq_num)
        try:
            ack, server = client_socket.recvfrom(1500)
            print("ACK received")
            break           #Stops trying to send the packet when it receives an ACK
        except timeout:     #Sends packet again if the transmission times out
            print("REQUEST TIMED OUT")
            retransmission_count += 1

    if retransmission_count == 6:   #Occurs if packet wasn't transferred after 6 tries
        break                       #End transfer
    
    seq_num = 1 - seq_num           #Updates sequence number for next packet
    
    if len(data) < 512:             #Checks if client has reached the end of the file (includes check for 0 byte packet if file is integer multiple of 512)
        end_time = time.time()
        rtt = end_time - start_time #Calculates total time file transfer took
        successful_transfer = True
        end_found = True

time.sleep(1)   #Delays the progam 1 second so server can complete the transfer

if filecmp.cmp('inputfile.txt', 'outputfile.txt') == True:  #Compares input and output files to make sure the transfer worked correctly
    print("sFTP: file sent successfully to", host_ip_address, "in", format(rtt, '.3f'), "secs")
else:
    print("sFTP: file transfer unsuccessful: packet retransmission limit reached")
input_file.close()