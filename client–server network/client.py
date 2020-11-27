import socket

s = socket.socket()
connected = False

def getinput():
    global s
    global connected
    message = input('>>> ')
    if message == '/join':
        if connected == False:
            joinserver()
        else:
            getinput()
    elif message == '/leave':
        if connected == True:
            s.close
        else:
            getinput()
    else:
        s.send(message.encode('utf-8'))

def listen():
    global s
    data = s.recv(1024)
    message = data.decode('utf-8')
    print(message)
    getinput()
    listen()

def joinserver():
    global s
    global connected
    ip = input('Enter IP:\n')
    port = input('Enter Port:\n')
    unstr = input('Enter username:\n')
    s.connect((ip, int(port)))
    username = ('/un' + unstr)
    s.send(username.encode('utf-8'))
    connected = True
    getinput()
    listen()

getinput()
