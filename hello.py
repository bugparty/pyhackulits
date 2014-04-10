#coding:gbk
__author__ = 'bowman'

import urllib2
import httplib
import re
conn = httplib.HTTPConnection('tw.heuet.edu.cn:80')
conn.request('GET','/admin/login.asp')
res = conn.getresponse()
print res.status
body =  res.read()
sample_str = '''< font
face = "Arial, Helvetica, sans-serif" >
6689
< / font >'''

capcha_re =\
    re.compile('< font\nface \= \"Arial\, Helvetica\, sans-serif\" \>\n(\d{4})')
sample2 =\
        '<font face="Arial, Helvetica, sans-serif"> \r\n              6479\r\n'
cap =\
    re.compile('<font face\=\"Arial\, Helvetica\, sans-serif\"> \r\n              (\d+)\r\n')
m2 = cap.match(sample2)
img = re.compile('<img')
m3 = img.match(body)
