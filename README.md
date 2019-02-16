#TCP-server
import socket

#创建套接字
sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#绑定地址
sockfd.bind(('0.0.0.0',8888))

#设置监听
sockfd.listen(5)

#消息收发
def recv_and_send(connfd,addr):
    while True:
        data = connfd.recv(1024)
        if data.decode() == '##':
            connfd.send('Bye'.encode())
            return
        else:
            print('Receive message:',data.decode())
            n = connfd.send('Receive your massage!!'.encode())
            print('Send %d bytes'%n)
#等待处理客户端连接
while True:
    print('Waitting for Connect...')
    connfd,addr = sockfd.accept()
    print('Connect from',addr) #客户端地址
    recv_and_send(connfd,addr)



#关闭连接
connfd.close()
sockfd.close()


