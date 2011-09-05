import os
import random

def source(fname):
	"""Read the specified file and execute the Python code
	"""
	new_fname = os.path.realpath(os.path.expanduser(fname))
	if os.access(new_fname, os.F_OK):
		fd1 = open(new_fname, "r")
		flines = fd1.readlines()
		s = ""
		for f in flines:
			s += f
			#print(s)

		print('*************************** starting ' + fname)
		exec(s)
	else:
		print('File not found ' + new_fname)
	return(0)


debug = 0

def dprint( txt):
	global debug
	if debug > 0:
		print(txt)
	return(0)


from SBList import *
l = [1,2,6,3,12,7]
sl = SBList(l)

# check the list length routine:
assert(sl.get_llen(0) == 6)

m = []
for n in sl:
  m.append(n)

assert(m == l)

sl.insert(2, 99)
assert(sl.get_llen(1) == 7)
assert(sl.get_llen(0) == 6)
sl.insert(2, 98)
sl.insert(7, 88898)
sl.undo()

assert(sl.get_lrow_idx(0) == 0)
assert(sl.get_lrow_idx(1) == 1)
assert(sl.get_lrow_idx(2) == 7)
assert(sl.get_lrow_idx(3) == 6)
assert(sl.get_lrow_idx(4) == 2)
assert(sl.get_lrow_idx(5) == 3)
assert(sl.get_lrow_idx(6) == 4)
assert(sl.get_lrow_idx(7) == 5)

m = []
for n in sl:
  m.append(n)

assert(m == [1, 2, 98, 99, 6, 3, 12, 7])

source('./SBLtest01.py')
source('./SBLtest02.py')
source('./SBLtest03b.py')
source('./SBLtest04.py')
source('./SBLtest05.py')
source('./SBLtest06.py')
source('./SBLtest07.py')
source('./SBLtest03.py')
source('./SBtest02.py')
source('./SBStest01.py')
source('./SBStest02.py')
source('./SBStest03.py')

