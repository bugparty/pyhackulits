#coding:utf8
__author__ = 'bowman'
#automatic page get/head requester
import thread,time
import httplib
alive = 0
limit = 100
aliveLock = thread.allocate_lock()
finished = 0
succeed = 0
fLock = thread.allocate_lock()
lockP = thread.allocate_lock()
def do(id):
    global alive
    global finished,succeed
 
    aliveLock.acquire()
    alive += 1
    aliveLock.release()
 
 
    conn = httplib.HTTPConnection('tw.heuet.edu.cn:82')
    conn.request('HEAD', '/View.asp?id=%i' % id)
    res = conn.getresponse()
 
    fLock.acquire()
    if res.status == 200:
        succeed += 1
    else:
        lockP.acquire()
        print res.status
        print res.getheaders()
        lockP.release()
    finished += 1
    alive -= 1
    fLock.release()
    thread.exit_thread()
 
def runner(id,ticks):
    global alive
    global finished,succeed,limit
    i=0
    end = ticks
    runs=0
    limit = 2
    z =0
    prevz = False
    ten = 0
    while i < end:
        if alive < limit:
            thread.start_new_thread(do,(6,))
            i+=1
        time.sleep(1.0/limit)
        runs += 1.0/limit
        if runs > 0.5:
 
            if alive ==0:
                if prevz:
                    z+=1
 
                prevz = True
            else:
                prevz = False
 
            if alive >4:
 
                ten +=1
            if z>=5:
                z = 0
                limit +=1
                print 'limit+',limit
            if ten >=10:
                ten = 0
                if limit > 5:
                    limit -=1
                    print 'limit-',limit
 
            print "%s\t%s\t%s\t" % (finished, alive, succeed)
            runs =0
import sys
if __name__ == '__main__':
    if len(sys.argv)!= 3:
        print '''%s yourid visits
for example:
cowpower.py 6 2000
代表替id为6的同学刷2000次访问
'''% sys.argv[0]
    else:
        id = int(sys.argv[1])
        ticks = int(sys.argv[2])
        print 'id',id,'ticks',ticks
        print '线程完成数\t当前活动线程\t成功提交数\t'
        runner(id,ticks)
