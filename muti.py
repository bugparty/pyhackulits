__author__ = 'bowman'
import thread
import time
succeed = 0
alive = 0
second_limit = 50
thread_interval = 0.1
total_task = 1000
succLock = thread.allocate_lock()
aliveLock = thread.allocate_lock()
def do(host,url):
    global succeed
    global alive
    aliveLock.acquire()
    alive += 1

    while True:
        if alive < second_limit:
            print 'alive',alive
            break
        else:
            time.sleep(thread_interval)


    aliveLock.release()
    print 'aliveLock released'
    succLock.acquire()
    print 'succLock acquired'
    succeed +=1
    succLock.release()
    print 'succLock released'
    aliveLock.acquire()
    alive -= 1
    print 'alive released',alive
    aliveLock.release()
    thread.exit_thread()

def run():
    for i in range(1,total_task):

        thread.start_new_thread(do,('tw.heuet.edu.cn:82','/View.asp?id=8'))



if __name__ == '__main__':

    run()
    while True:
        print 'succeed',succeed
        if succeed >= total_task-1:
            break
        time.sleep(0.5)
    


