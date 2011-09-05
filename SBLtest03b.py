# test the undo list for sort, include sorting something
# that is already in sort order.
from SBList import *
import difflib, random, sys
#####################################################################
def subsort(lst, start, end):
	"""sort a regular list object between the starting
	and ending python offsets (the value of *end* is
	used as an array index capturing value n-1)
	"""
	lstart = l[0:start]
	lend = l[end:]
	lmid = l[start:end]
	lmid.sort()
	final = []
	final.extend(lstart)
	final.extend(lmid)
	final.extend(lend)
	return(final)

l = ['a', 'g','e', 't','g','h','b','n']

q = SBList(l)
q.sort()
q.sort()
q.sort()
q.sort()
q.sort()
print(repr(q.get_undo_list()))
#####################################################################
#
#                          Testing
#
######################################################################
# generate an auto-correlated series of characters to test the
# sort routine.  The challenge is to sort a subset of input rows
# when the old sate ranges spand into or across the sort region
# of a subsort
replicates = 3000
str_len = 20
#
#print('\n---------------------------------------------------')
#print('Test module: ' + sys.argv[0])
#print('starting ' + str(replicates) + 'replications of sorting with ' \
#      + 'string length of ' + str(str_len))
#for j in range(replicates):
#	l = []
#	l.append(chr(random.randint(ord('a'), ord('z'))))
#	j = 0
#	while j < str_len:
#		r = random.randint(0, 20)
#		if r < 2:
#			# generate an autocorrelated string 
#			k_max = random.randint(1, 4)
#			k = 0
#			l.append(l[-1])
#			while j < str_len and k < k_max:
#				l.append(l[-1])
#				k += 1
#				j += 1
#		else:
#			l.append(chr(random.randint(ord('a'), ord('z'))))
#		j += 1
#	#
#	# Now copy the list and test it
#	#
#	start_offset = random.randint(0, str_len - 3)
#	end_offset = random.randint(start_offset + 1, str_len - 1)
#	save_l = []
#	save_l.extend(l)
#	q = SBList(l)	
#	q.sort(start=start_offset, end=end_offset)
#	l_new = q.return_list()
#	save_l2 = subsort(save_l, start_offset, end_offset)
#	# The diff() function seems to remove the sort from
#	# my saved list
#
#	### TEMPORARY HACK TO TEST ERROR DETECTION:
#	##save_l2[3] = 'zzTEST'
#	difflist = list(difflib.ndiff(save_l2, l_new))
#	if len(difflist) != len(q):
#		print('================== verify failed')
#		print("start idx " + str(start_offset) + ' end idx ' + str(end_offset))
#		print('save:\n' + repr(save_l2))
#		print('new:\n' + repr(l_new))
#		raise Exception('Verify failed')
#print('finished with no errors')


