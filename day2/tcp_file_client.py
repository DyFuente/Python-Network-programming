from socket import *
from time import sleep

s = socket()
server_addr = ('127.0.0.1',8080)
s.connect(server_addr)
while True:
    try:
        f_name = input('请输入文件名称:')
    except NameError:
        print('请规范输入!')
    if not f_name:
        break
    s.send(f_name.encode())#发送文件名
    data2 = s.recv(1024)
    print(data2.decode())
    try:
        f_read = open(f_name,'rb')
        while True:
            data = f_read.read(1024)
            s.send(data)
            sleep(0.2)
            if not data:
                s.send('##'.encode())
                print('传输完成')
                break
    except Exception as e:
        print('error!')
        print(e)
    finally:
        f_read.close()

s.close()
    

