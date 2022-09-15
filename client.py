import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 48763

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

end = False

def sendMsg():
    global end
    time.sleep(0.5)
    while True:
        time.sleep(0.5)
        if end == True:
            break
        cmd = input("Please input command:\n")
        try:
            server.send(cmd.encode())
        except:
            break
        if cmd == "exit":
            end = True
            break

def receiveMsg():
    global end
    while True:
        data = server.recv(48763)
        print("server:",data.decode())
        if data.decode()=="bye":
            end = True
        if end == True:
            break

t1 = threading.Thread(target=receiveMsg)
t2 = threading.Thread(target=sendMsg)
t1.start()
t2.start()
t1.join()
t2.join()

server.close()