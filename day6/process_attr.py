from multiprocessing import  Process 
from time import sleep,ctime

def tm():
    for i in range(3):
        sleep(2)
        print(ctime())

p = Process(target=tm,name="wazi")
#查看子进程是否在生命周期
print('alive:',p.is_alive())
p.daemon =True
p.start()

#进程名称
print('Process name',p.name)
#对应子进程的PID号
print('Process PID',p.pid)
print('alive:',p.is_alive())

p.join(2)
print("====================")