#服务端
from socket import *

s= socket()
s.bind(('0.0.0.0',14325))
s.listen(5)

c,addr = s.accept()
print('Connect from:',addr)

f = open('leg.png','wb')
while True:
    data = c.recv(1024)
    if not data:
        break
    f.write(data)
f.close()
c.close()
s.close()
