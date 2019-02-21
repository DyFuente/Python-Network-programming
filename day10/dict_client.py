from socket import * 
import sys 
import getpass 

#创建网络连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return 
    host = sys.argv[1]
    port = int(sys.argv[2])
    addr = (host,port)

    #创建套接子
    s = socket()
    try:
        s.connect(addr)
    except Exception as e:
        print(e)
        return 
    
    #进入一级界面
    while True:
        print('''
        ========Welcome========
        --1.注册  2.登录  3.退出--
        =======================
        ''')

        cmd = input("输入选项>>")
    
        if cmd not in ['1','2','3']:
            print("请输入正确选项")
            sys.stdin.flush() #清除标准输入
            continue 
        elif cmd == '1':
            do_register(s) #注册功能

def do_register(s):
    while True:
        name = input("User:")
        passwd = getpass.getpass()
        passwd1 = getpass.getpass("Again:")

        if (' ' in name) or (' ' in passwd):
            print("用名或密码不能有空格")
            continue 
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        
        msg = "R %s %s"%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print('注册成功')
        elif data == 'EXISTS':
            print('用户已存在')
        else:
            print("注册失败")
        return

main()