import socket
  
s = socket.socket()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print('Server made on ' + ip_address)

s.bind((ip_address, 0))         
print('Server binded to port', s.getsockname()[1])
  
s.listen(2)      
print('Server is listening.')

c, addr = s.accept()      
print('Got connection from', addr)

clients = []
usernames = []
clients.append(c)

while True:
   data = c.recv(1024)
   strdata = data.decode('utf-8')
   if not data:
      c.close
   elif strdata[:3] == '/un':
      print('Got username from', addr)
      usernames.append(strdata[3:len(strdata)])
   else:
      print('Got data ' + strdata + ' from', addr)
      usernum = clients.index(c)
      message = ('<' + str(usernames[int(usernum)]) + '> ' + strdata)
      for i in clients:
         i.send(message.encode('utf-8'))
