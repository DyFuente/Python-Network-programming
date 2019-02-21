from threading import Thread
from time import sleep

def fun():
    sleep(3)
    print('线程属性测试')

t = Thread(target=fun,name='Iron man')

#线程名称
t.setName('一拳超人')
print('Thread name:',t.name)
print('Thread name:',t.getName())

#设置daemon为True
t.setDaemon(True)

t.start()
#查看线程生命周期
print("alive:",t.is_alive())


# t.join()