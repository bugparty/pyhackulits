__author__ = 'bowman'
import cPickle

a = 'a'
b = 1
l = (a,b)
f = open('dump','w')
cPickle.dump(a,f,cPickle.HIGHEST_PROTOCOL)
cPickle.dump(b,f,cPickle.HIGHEST_PROTOCOL)
cPickle.dump(l,f,cPickle.HIGHEST_PROTOCOL)
f.close()
f = open('dump','r')

da = cPickle.load(f)
db = cPickle.load(f)
print da,db