import socket

#创建套接字
sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#绑定地址
sockfd.bind(('0.0.0.0',8888))

#设置监听
sockfd.listen(5)

#等待处理客户端连接
while True:
    print('Waitting for Connect...')
    try:
        connfd,addr = sockfd.accept()
    except KeyboardInterrupt:
        print('Server exit')
        break
    print('Connect from',addr) #客户端地址
    #消息收发
    while True:
        data = connfd.recv(1024)
        if data.decode() == '##':
            connfd.send('Bye'.encode())
            break
        else:
            print('Receive message:',data.decode())
            n = connfd.send('Receive your massage!!'.encode())
            print('Send %d bytes'%n)
    connfd.close()
#关闭连接
sockfd.close()

