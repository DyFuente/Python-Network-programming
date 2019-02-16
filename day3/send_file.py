#客户端
from socket import *

s = socket()
s.connect(('127.0.0.1',14325))

filename = input('请输入文件名称:')
f = open(filename,'rb')

while True:
    data = f.read(1024)
    if not data:
        break
    s.send(data)

f.close()
s.close()