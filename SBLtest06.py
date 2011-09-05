from SBList import *
# test of get_undo_list() and get_state_id()
import sys, random
print('------------------------------------------------------------')
print(sys.argv[0])

######################################################################
# This is an attempt to test SBList by generating random strings
# then inserting strings with numbers so that I can look for those
# numbers in the undo list.
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
replicates = 300
max_list_len = 30
max_str_len = 20
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
	insert_idx = []
	for j in range(inserts):
		#### EXPAND THIS LATER TO ALLOW LST_LEN OR MORE:
		insert_idx.append(random.randint(0, list_len - 1))
	#
	planned_inserts = []
	# Now perform the inserts
	for j in range(inserts):
		# insert to the SBList and the parallel regular list
		new_s = random_string(random.randint(1, max_str_len)) \
			+ 'insrt{0:05d}'.format(j)
		q.insert(insert_idx[j], new_s)
		planned_inserts.append(['i', insert_idx[j]])
	u = q.get_undo_list()
	for j in range(len(u)):
		assert(u[j][3] == planned_inserts[j][1])

	# Now cycle through the inserts using the undo list to
	# see if I can find the numbers that I inserted with 
	# the 'insrt{0:05d}' command above
	print('The main list is:\n' + repr(q).replace(',', '\n'))
	print('Planned inserts were: ' + repr(planned_inserts))
	print('The undo list is ' + repr(u))
	u_len = len(u)
	for j in range(0, u_len):
		# u is the undo list
		#print(u[j].get_new()[-5:] + '  -  ' + str(u[j].get_state_id()))
		assert(int(u[j].get_new()[-5:]) == u[j].get_state_id())
print("finished OK")
