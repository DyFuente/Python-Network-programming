from socket import *

#创建数据报套接字
sockfd = socket(AF_INET,SOCK_DGRAM)

#绑定地址
server_addr = ('0.0.0.0',14325)
sockfd.bind(server_addr)

#消息收发
while True:
    try:
        data,addr = sockfd.recvfrom(1024)
    except KeyboardInterrupt:
        print('服务器退出')
    print('Connect from %s:%s'%(addr,data.decode()))
    sockfd.sendto('古德古德'.encode(),addr)

#关闭套接字
sockfd.close()
