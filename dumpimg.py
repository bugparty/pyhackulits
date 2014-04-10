__author__ = 'bowman'
import urllib2
import Queue
import threading
import time
#configurations
usingProxy = True
mycookie = r"ASP.NET_SessionId=hja3rn45jcvqk155hlxsib45; CNZZDATA4809044=cnzz_eid%3D148487762-1387383541-http%253A%252F%252Fjwc.heuet.edu.cn%252F%26ntime%3D1397071030%26cnzz_a%3D16%26sin%3Dnone%26ltime%3D1397071026368%26rtime%3D8"
#end of configuration

test_id = 201109111101
gae_proxy  = urllib2.ProxyHandler({'http':'127.0.0.1:8087'})
proxyedOpener = urllib2.build_opener(gae_proxy)
lockL = threading.RLock()
flog = open("imgdumplog.txt","a")

if usingProxy:
    urllib2.install_opener(proxyedOpener)
else:
    pass
global idqueue
global total
def dumpimg(picid,prefix='imgs',server_prefix='xk1'):
    global mycookie,lockL
    req = urllib2.Request("http://%s.heuet.edu.cn/readimagexs.aspx?xh=%s" % (server_prefix,picid))
    req.add_header('Cookie',mycookie)

    response = urllib2.urlopen(req)
    img = response.read()
    f_img = open(prefix+'/%s.jpg'% picid.rstrip('\n'),"wb")
    f_img.write(img)
    f_img.close()
def dumpimg2(picid):
    global mycookie,lockL
    req = urllib2.Request("http://xk2.heuet.edu.cn/readimagexs.aspx?xh=%s" % picid)
    req.add_header('Cookie',mycookie)

    response = urllib2.urlopen(req)
    img = response.read()
    f_img = open('imgs/%s.jpg'% picid.rstrip('\n'),"wb")
    f_img.write(img)
    f_img.close()


class Worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        global flog,lockL
        while True:
            id = self.queue.get()
            try:
                dumpimg(id)
            except urllib2.URLError as e:
                lockL.acquire()
                flog.write("URLError id:%s\n"%id)
                flog.write(str(e)+"\n")
                lockL.release()
            finally:
                self.queue.task_done()

def init_queue(startfrom=0):
    print 'started from %i'%startfrom
    global idqueue,total
    print 'feeding queue'
    f = open('cardno.txt', 'r')
    lines = f.readlines()
    lines = lines[startfrom:]
    total = len(lines)
    current = 0
    percent = total / 100
    idqueue = Queue.Queue(total+10)
    for i in  zip(lines,range(0,total)):
        idqueue.put(i[0])
        if(i[1]> current+percent):
            current = i[1]
            #print type(current)
            print "queue loading %3.0f%%\t " % (current*100.0/total)
    print "queue loading %3.0f%%\t " % (100.0)
    print 'feeded queue'
def init_worker(threads=10):
    global idqueue
    print 'start deamons'
    for i in range(0,threads):
        t = Worker(idqueue)
        t.setDaemon(True)
        t.start()
        print 'deamon %i launched'%i

    print 'deamon launched'

if __name__ == '__main__':
    #dumpimg(str(test_id),prefix='.',server_prefix='xk1')
    init_queue(238373+8000)
    init_worker(threads=130)
    totali = int(total)
    last =0
    while not idqueue.empty():
        downloads = totali - idqueue.qsize()
        persec = downloads -last
        print 'downloaded %i pics,%ipic/s,percent %03.3f%%'% (downloads,persec/2,downloads*100.0/totali)
        last = downloads
        time.sleep(2)






