__author__ = 'bowman'
import thread,time

alive = 0
aliveLock = thread.allocate_lock()
finished = 0
fLock = thread.allocate_lock()

def do():
    global alive,finished
    aliveLock.acquire()
    alive += 1
    while True:
        if alive > 50:
            time.sleep(0.1)
        else:
            break

    alive -= 1
    print 'do my workings'
    aliveLock.release()
    fLock.acquire()
    finished+=1
    fLock.release()
    thread.exit_thread()

for i in range(1,1000):
    thread.start_new_thread(do,())

global alive
while True:

    print finished
    time.sleep(0.5)

