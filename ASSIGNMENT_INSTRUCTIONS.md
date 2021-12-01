Part B: Stop-and-Wait File Transfer
In this part, we will develop a simple unidirectional file transfer application over UDP.
Our goal would be to make it as simple as possible, while ensuring correctness/reliability
of the file transfer. It will be built along the lines of the Stop-and-Wait reliable transfer
protocol (Rdt 3.0) that we studied in Chapter 3. The requirements that the application
(which we will call sftp) must satisfy are described below.

The sftp application requirements:
The data transfer will be unidirectional – from the client to the server, although the
acknowledgements would need to be sent from the server to the client. To transfer a file, 
the user (client) should call sftpClient <server_ipaddress> where server_ipaddress is the
IP address of the server in dotted decimal format. The stop-and-wait version of the
protocol that you will implement has some similarities with the Trivial FTP (or TFTP)
protocol, that also runs over UDP. In a way, the sftp application that you will implement
can be viewed as a simpler version of TFTP.

  • When called, sftp will read a file called inputfile from the local directory, and
  transfer file in packets (each of which should contain 512 bytes of data, except
  possibly the last packet) using UDP sockets.

  • The server will reassemble the data in the packets into the file and write it as
  outputfile in the current working directory (an existing file with the same name
  will be rewritten).

  • There is no explicit connection setup and closing (unlike TCP). The first packet
  containing file data implicitly “sets up the connection”, so to speak. The end of
  the file is indicated by the transfer of a packet with less than 512 bytes of data;
  this also implicitly “closes the connection”, so to speak. So, no SYN or FIN flags
  are needed. (What if the file size is an integral multiple of 512 bytes? Well, then
  the client sends an additional packet with just 0 bytes of data to indicate the end of
  file!) Note that this is similar to the way TFTP implicitly sets up/closes the
  “connection”, and indicates the end of the file.

  • Like Rdt3.0, you can use only one-bit (0-1) sequence and acknowledgment
  numbers. You can allocate a full byte for it, for convenience, but the value of that
  byte can only be 0 or 1. Thus the data part of each UDP packet sent from the
  client to the server can be 513 bytes (1 byte header just indicating the 0-1
  sequence number, plus the 512 bytes of file data), except possibly for the last
  packet. The data part of each UDP packet sent from the server to the client can
  just be the 1 byte header just indicating the 0-1 acknowledgment number. You
  will assume that no bit errors happen in either forward or backward direction, so
  no checksum needs to be included in any packet.

  • The client can use any ephemeral port number, but the server must listen on port
  number 9093. The client’s retransmission timer should be set to 1 sec. The
  retransmission limit, of the maximum number of times that the client will attempt
  retransmitting a packet on timeout, should be set to 5, i.e., a total of six
  transmission attempts per packet.

  • Note that for sftp, you need to write both client and server (no code will be
  provided), sftpClient.java and sftpServer.java. However, feel free to borrow
  inspiration and code that you wrote for the ping application in Part A of this
  assignment! You server should implement a LOSS_RATE and
  AVERAGE_DELAY, as in the ping application in part A.
  
  • You should test your code for different file sizes, but we ask you to report the
    results (see “Deliverables” below) for a fixed file size of 50 Kbytes.
    
  • You need to time the file transfer, and provide that in the output. For that the
  client can start a timer just before it starts sending the file data, and stop it when
  the entire file is transferred. If the file is transferred successfully, the client prints
  the following line:
    sFTP: file sent successfully to <server-ip-address> in <time in secs> secs
  If the file transfer fails due to retransmission limit being reached for some packet,
  the client prints the following line:
   sFTP: file transfer unsuccessful: packet retransmission limit reached
   
  • Make sure you compare inputfile and outputfile (bitwise comparison, not just the
  size) to make sure the file is transferred correctly from the client to the server.
