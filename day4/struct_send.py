from socket import *
import struct

ADDR = ('127.0.0.1',14325)
sockfd = socket(AF_INET,SOCK_DGRAM)

while True:
    id = int(input('id:'))
    name = input('name:')
    height = float(input('hight:'))
    length = len(name)

    fmt = "i16sf"
    data = struct.pack(fmt,id,name.encode(),height)
    sockfd.sendto(data,ADDR)
sockfd.close()

