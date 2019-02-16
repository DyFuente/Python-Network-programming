from socket import * 

s = socket()
s.bind(('0.0.0.0',8080))
s.listen(10)

while True:
    print('Waiting for Connect')
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        print('Server exit')
        break
    print('Connect from',addr) #客户端地址
    data = c.recv(128) #接收文件名
    filename = 'from_client_'+data.decode()
    print('创建文件名:',filename)
    n = c.send('success get name,wait the file'.encode())
    while True:  #循环接收文件内容
        data = c.recv(1024)
        if data.decode() == '##':
            break
        else:
            try:
                file = open(filename,'wb')
                file.write(data)
            except Exception as e:
                print(e)
                print('传输错误')
                c.send('传输失败'.decode())
            finally:
                file.close()  
    c.close()
#关闭连接
s.close()



