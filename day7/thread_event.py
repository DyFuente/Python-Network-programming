from threading import Thread,Event
from time import sleep


e = Event()
#全局变量,用于通信
s = None

def foo():
    print("Foo 前来拜山头")
    global s
    s = "天王盖地虎"
    e.set() #设置e

f = Thread(target=foo)
f.start()

#主线程用来验证口令
print("口令!!!!!")
e.wait()    #添加阻塞
if s == '天王盖地虎':
    print('确认过眼神,你是对的人')
else:
    print('二营长,开炮!!!')

f.join()