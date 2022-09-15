import socket
import threading
import time
import datetime

bind_ip = "127.0.0.1"
bind_port = 48763

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

clientList = []
readyList = []
hitList = []
end = False
allHit = False
zeroHit = True
firstHit = datetime.datetime.now()
lastHit = datetime.datetime.now()

print("[*] Listening on",bind_ip,bind_port)

def clientThread(client, addr):
    global zeroHit, allHit, end, firstHit, lastHit
    msg = "Welcome to this room! The number of people("+str(len(clientList))+"/5)\nYou are player "+str(len(clientList)-1)
    client.send(msg.encode())
    clientIndex = len(clientList)-1
    while True:
        try:
            data = client.recv(48763)
            message = data.decode()
            if message == "ready":
                readyList[clientIndex] = 1
                broadcast("Player "+str(clientIndex)+" is ready!" )
                print("Player "+str(clientIndex)+" is ready!" )
                hitCheck = True
                for s in readyList:
                    if s == 0:
                        hitCheck=False
                        break
                if hitCheck==True:
                    broadcast("Players are all ready! Game start!")
                    print("Players are all ready! Game start!")
            elif message == "exit":
                end = True
                break
            elif message == "hit":
                hitCheck = True
                for s in readyList:
                    if s == 0:
                        hitCheck=False
                        break
                if hitCheck==False:
                    broadcast("Players are not ready!")
                elif hitCheck==True:
                    allHitCheck = True
                    hitList[clientIndex] = 1
                    for c in hitList:
                        if c==False:
                            allHitCheck = False
                            break
                    if allHitCheck == True:
                        allHit = True
                    localtime = time.localtime()
                    result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
                    broadcast("Player "+str(clientIndex)+" hit! The time is "+result)
                    print("Player "+str(clientIndex)+" hit! The time is "+result)
                    if zeroHit == True:
                        broadcast("first hit is Player "+str(clientIndex))
                        print("first hit is Player "+str(clientIndex))
                        firstHit = datetime.datetime.now()
                        zeroHit = False
                        time.sleep(0.05)
                    if allHit == True:
                        broadcast("last hit is Player "+str(clientIndex))
                        print("last hit is Player "+str(clientIndex))
                        lastHit = datetime.datetime.now()
                        time.sleep(0.01)
                        timeInterval = (lastHit-firstHit).seconds
                        broadcast("You all hit in "+str(timeInterval)+" seconds!")
                        print("You all hit in "+str(timeInterval)+" seconds!")
                        time.sleep(0.01)
                        broadcast("bye")
                        for s in clientList:
                            s.close()
                        server.close()
                        break
            else:
                print(addr, ":", message)
        except:
            break

def broadcast(msg):
    for s in clientList:
        s.send(msg.encode())

while True:
    try:
        client, addr = server.accept()
        clientList.append(client)
        readyList.append(0)
        hitList.append(0)
        print(addr, "is connected!")
        print(len(clientList),"player in this room now")
        t=threading.Thread(target=clientThread, args=(client, addr))
        t.start()
    except:
        break