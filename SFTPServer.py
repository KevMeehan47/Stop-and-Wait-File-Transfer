import time
import random
from socket import *

port_num = 9093
print("Running on port:", port_num)

server_socket = socket(AF_INET, SOCK_DGRAM) #Creates UDP socket  
server_socket.bind(('', port_num))
server_socket.settimeout(1)                 #Waits 1 second for reply before timing out
LOSS_RATE = .3                              #Loss Rate in percentage (.01 = 1%)
AVERAGE_DELAY = 100                         #Average delay in ms

file = open("outputfile.txt", 'w')

end_of_file = False                         #Represents if the end of the read file is found
ack = 1                                     #Declare the ack variable as the opposite of what the first seq_num variable will be
while True:
    try:
        packet, address = server_socket.recvfrom(1500)  #Receives packet and address from the client
        if file.closed == True:                         #Checks if the file hasn't been opened yet
            file = open("outputfile.txt", 'w')
        
        if len(packet) < 513:       #Checks if the last packet has been transmitted
            end_of_file = True
            
    except timeout:     #If the system times out, restart the loop
        continue
    
    rand = random.uniform(0, 1)     
    if rand < LOSS_RATE:            #Simulates the percentage chance of packet loss
        print("Packet not received")
        continue
    
    ack = packet.decode()[-1]                               #Saves the last byte of the packet (the sequence number) as the new ACK
    server_socket.sendto(str.encode(str(ack)), address)     #Sends the ACK back to the client
        
    data = packet.decode()[:-1]     #Saves the rest of the packet as the data
    file.write(data)                #Writes the data to the output file
    
    delay = random.randint(0.0, 2*AVERAGE_DELAY)    #Randomly generates delay
    time.sleep(delay/1000)  
    
    print("ACK sent")
    
    if end_of_file:
        #Corrects the glitch that makes every skipped line turn into two skipped lines
        print("End of file")
        #Gets rid of extra blank lines in output file
        file = open("outputfile.txt", 'r')
        file_data = file.read()
        file_data = file_data.replace('\n\n', '\n')
        file = open("outputfile.txt", 'w')
        file.write(file_data)
        file.close()
        end_of_file = False