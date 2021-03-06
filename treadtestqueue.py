#!/usr/bin/python3
#Python 的 Queue 模块中提供了同步的、线程安全的队列类，包括
# FIFO（先入先出)队列Queue，
# LIFO（后入先出）队列LifoQueue，
# 和优先级队列 PriorityQueue。
#这些队列都实现了锁原语，能够在多线程中直接使用，可以使用队列来实现线程间的同步

import queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    """
    parameters:
    q; work Queue
    
    """
    def __init__(self,threadID,name,q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print("开启线程："+self.name)
        process_data(self.name,self.q)
        print("退出线程："+self.name)
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing  %s" %(threadName,data))
        else:
            queueLock.release()
        time.sleep(1)
threadList = ["Thread-1","Thread-2","Thread-3"]
nameList = ["One","Two","Three","Four","Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

#创建新线程
for tName in threadList:
    thread = myThread(threadID,tName,workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
#填充队列
queueLock.acquire()
for work in nameList:
    print("开始装入work:"+work)
    workQueue.put(work)
queueLock.release()

#等待队列清空
while not workQueue.empty():
    pass

#通知线程是时候退出
exitFlag = 1

#等待所有线程完成 threads所有join入的线程执行完毕后，主线程才会继续执行
for t in threads:
    t.join()

print("退出主线程")




