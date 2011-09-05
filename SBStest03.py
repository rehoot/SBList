from SBStrList import *

from SBList import *
# test SBStrList iteration
print('########### starting SBSTest03.py')
###########################
l = ['aaa', 'bbb', 'ccc', 'ddd']
###########################
sbl = SBList(l)
m = []
for a in sbl:
	#print(repr(a))
	m.append(a)

assert(m == l)
##################
sb = SBStrList(l)

m = []
for a in sb:
	#print(a.get_string())
	m.append(a.get_string())

assert(m == l)
###########################
l = ['aaa\n', 'bbb\n', 'ccc\n', 'ddd\n', 'ee\n', 'ff\n', 'ggg\n']
###########################
sbl = SBList(l)
m = []
for a in sbl:
	#print(repr(a))
	m.append(a)

assert(m == l)
##################
sb = SBStrList(l)

m = []
for a in sb:
	#print(a.get_string())
	m.append(a.get_string())

assert(m == l)
