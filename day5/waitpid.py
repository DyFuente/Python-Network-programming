import os 
from time import sleep

pid = os.fork()

if pid < 0:
    print("Error")
elif pid == 0:
    sleep(3)
    print("Child %d process exit"%os.getpid())
    os._exit(2)
else:
    #非阻塞等待
    while True:
        p,status = os.waitpid(-1,os.WNOHANG)
        if p != 0:
            break
        sleep(1)
        print('Do something instead')
    while True:
        print('完成父进程的其他事件')
        sleep(2)

