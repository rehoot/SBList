#####################################################################
# SBtest04.py: test insert()
#                          Testing
#
######################################################################
from SBList import *
import difflib, random, sys

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
######################################################################
# generate an auto-correlated series of characters to test the
# sort routine.  The challenge is to sort a subset of input rows
# when the old sate ranges spand into or across the sort region
# of a subsort
replicates = 300
max_list_len = 300
max_str_len = 200
#
print('\n-----------------------------------------------------')
print('Test module: ' + sys.argv[0])
print(str(replicates) + 'replications')
for j in range(replicates):
	# defining the seed here will help me to reproduce the 
  # the exact experiment if it fails
	myseed = random.random()
	random.seed(a=myseed)
	list_len = random.randint(5, max_list_len)
	max_str_len = random.randint(5, max_str_len)
	inserts = random.randint(1, int(list_len / 2))
	l = []
	l.append(chr(random.randint(ord('a'), ord('z'))))
	str_len = random.randint(1, max_str_len)
	s = ''
	for j in range(list_len):
		s = random_string(str_len)
		l.append(s)
	#
	# Now copy the list and test it
	# (I copy the list to avoid the possibility that some
	# testing operations will change the original list and
	# thereby ruin my ability to detect changes)
	#
	save_l = []
	save_l.extend(l)
	q = SBList(l)	
	for j in range(inserts):
		# insert to the SBList and the parallel regular list
		new_s = random_string(random.randint(1,max_str_len)) + 'insrt'
		loc = random.randint(0, len(q))
		q.insert(loc, new_s)
		save_l.insert(loc, new_s)
	#
	l_new = q.return_list()

	### TEMPORARY HACK TO TEST ERROR DETECTION:
	##save_l[3] = 'zzTEST'
	difflist = list(difflib.ndiff(save_l, l_new))
	if len(difflist) != len(q):
		print('================== verify failed')
		print('save:\n' + repr(save_l))
		print('new:\n' + repr(l_new))
		print('random number generator seed was ' + str(myseed))
		raise Exception('Verify failed')
print('finished with no errors')


