from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789
# Bind the socket to server address and server port
serverSocket.bind(('', serverPort))
# Listen to at most 1 connection at a time
serverSocket.listen(1)

while True:
    print('The server is ready to receive')
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()
        # Extract the path of the requested object from the message
        filename = message.split()[1]
        f = open(filename[1:])
        # Store the entire content of the requested file in a temporary buffer
        outputdata = f.read()
        f.close()

        # Send the HTTP response header line to the connection socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        connectionSocket.close()

serverSocket.close()
sys.exit()