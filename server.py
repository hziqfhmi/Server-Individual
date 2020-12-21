import socket
import threading
import subprocess
import os
import readline

PORT = 2222
connections = []
run = True

def _exit():
    global run
    global connections
    run = False
    for i in connections:
        i.send(b'exitsshserver')
        i.shutdown(socket.close())
        run = False
    exit(0)

def handler(conn):
    global connections
    while True:
        raw = conn.recv(4096)
        income = raw.decode("utf8")
        if income == "exit":
            conn.close()
            del connections[connections.index(conn)]
        else:
            try:
                if income.startswith("cd ") is False:
                    send = subprocess.check_output(income, shell=True)
                    print ('result = {}'.format(send))
                    conn.send(send)
                elif income.startswith("cd ") is True:
                    splitstr = income.split(" ")
                    print (os.chdir(splitstr[1]))
            except Exception as e:
                l = "INCORRECT COMMAND ERROR {}".format(e)
                conn.send(l.encode("utf8"))

def listen(PORT):
    global connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", PORT))
        s.listen(16)
        while True:
            conn, address = s.accept()
            connections.append(conn)
            print (connections)
            handlerThread = threading.Thread(target=handler, args=(conn,))
            handlerThread.setDaemon(True)
            handlerThread.start()

listenThread = threading.Thread(target=listen, args=(PORT,))
listenThread.setDaemon(True)
listenThread.start()

while run:
    try:
        var = input()
    except KeyboardInterrupt:
        _exit()
    except subprocess.CallProcessError() as e:
        print ("Sub Pro Error {}".format(e))
    except OSError:
        pass
