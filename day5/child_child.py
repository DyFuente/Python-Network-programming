# 创建二级子进程处理僵尸
#   1.父进程创建子进程,等待回收子进程
#   2.子进程创建二级子进程,然后退出
#   3.二级子进程成为孤儿,和原来父进程一同执行事件

import os
from time import sleep

def f1():
    sleep(3)
    print('吃元宵')

def f2():
    sleep(4)
    print("处理南北甜咸之争")

pid = os.fork()

if pid < 0:
    print("Error")
elif pid == 0:
    #创建二级子进程
    pid2 = os.fork()
    if pid2 == 0:
        f2()
    else:
        os._exit(0)
else:
    os.wait()   #等待一级子进程退出
    f1()

