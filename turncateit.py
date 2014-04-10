__author__ = 'bowman'
fin = open('cardnoraw.txt','r')
fout= open('cardno.txt', 'w')
print 'loding'
cardids = (line[1:-2] for line in fin.readlines())
print 'writing'
fout.write('\n'.join(cardids))
fout.close()
fin.close()