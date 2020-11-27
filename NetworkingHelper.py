import socket

s = socket.socket()
clients = []

class server:

    def create():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print('Server made on ' + ip_address)
        s.bind((ip_address, 0))         
        print('Server binded to port', s.getsockname()[1])

    def acceptconnections(num):
        global clients
        s.listen(num)      
        print('Server is listening.')
        c, addr = s.accept()      
        print('Got connection from', addr)
        clients = []
        clients.append(c)

    def sendtoall(message):
        for cl in clients:
            cl.send(message.encode('utf-8'))

    def listen():
        data = s.recv(1024)
        decoded_data = data.decode('utf-8')
        return decoded_data

class client:

    def joinserver(ip, port):
        s.connect((ip, int(port)))

    def listen():
        data = s.recv(1024)
        decoded_data = data.decode('utf-8')
        return decoded_data
