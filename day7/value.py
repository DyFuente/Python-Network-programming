from multiprocessing import Process,Value
import time
import random

#创建共享内存
money = Value('i',5000)

#操作共享内存
def man():
    for i in range(30):
        time.sleep(0.1)
        money.value += random.randint(1,1000)
        print(money.value)
def beautiful_girl():
    for i in range(30):
        time.sleep(0.1)
        money.value -= random.randint(100,900)
        print(money.value)
m = Process(target=man)
g = Process(target=beautiful_girl)
m.start()
m.join()
g.start()
g.join()

print("一月余额:",money.value)