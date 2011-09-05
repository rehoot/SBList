from SBList import *
import difflib, random, sys

replicates = 300
list_len = 20
######################################################################
#
def random_string(len):
	s = ''
	for k in range(len):
		space_test = int(random.expovariate(.5)) + 1
		if space_test > 5:
			s += ' '
		else:
			s += chr(random.randint(ord('a'), ord('z')))
	return(s)
	

######################################################################
for r in range(replicates):
	l = []
	for j in range(list_len):
		l.append(random_string(3))
	
	q = SBList(l)
	
	for j in range(len(l) + 1):
		#print(q._get_l_idx(j))
		sd = q._get_l_idx(j)
		for k in sd:
			assert(k is not None)



