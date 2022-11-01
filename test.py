
import socket
import time


host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
print('Type /q to quit')
print('Enter message to send')

#message = input(" -> ")  # take input
#time.sleep(1)
#client_socket.send(message.encode())
message = ""
while message.lower().strip() != '/q':
    if message != "":
        client_socket.send(message.encode())  # send message
        time.sleep(1)
        data = client_socket.recv(1024).decode()  # receive response

        for x in range(3):
            if data == "":
                client_socket.send(message.encode())  # send message
                data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = ""
    message = input(" -> ")  # again take input
    time.sleep(1)
    data = ""


client_socket.close()  # close the connection

