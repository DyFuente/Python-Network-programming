from socket import * 
import struct

#创建套接字
sockfd = socket(AF_INET,SOCK_DGRAM)
sockfd.bind(('0.0.0.0',14325))

#确定数据结构
st = struct.Struct('i16sf')

#循环接受数据
while True:
    data,addr = sockfd.recvfrom(1024)
    #解析数据
    data = st.unpack(data)

    print(data)

sockfd.close()

