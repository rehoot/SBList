from SBString import *
import random

replicates = 300
debug = 0

def dprint( txt):
	global debug
	if debug > 0:
		print(txt)
	return(0)

def testblock(q, action, start, txt='', del_count=-1):
	if action=='i':
		dprint('----------- inserting starting at ' + str(start) + ' txt=' + txt)
		s = txt
		l = []
		l.extend(q.get_string())
		l.insert(start, txt)
		q.insert(start, txt)
		dprint(''.join(l))
		dprint(q.get_string())
		assert(''.join(l) == q.get_string())
	if action == 'd':
		dprint('----------- deleting starting at ' + str(start) + ' count:' + str(del_count))
		s = txt
		l = []
		l.extend(q.get_string())
		#l.delete(start, del_count)
		del l[start: start + del_count]
		q.delete(start, del_count)
		dprint('l: ' + ''.join(l))
		dprint('q: ' + q.get_string())
		assert(''.join(l) == q.get_string())
	return(0)
	#print('*state: ' + q.show_state())
	#print('			012345678901234567890')
	#print('*str: ' + q.get_string())
	#print('- - - - - - - - - - ')
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

print('Running ' + str(replicates) + ' inserts and delete ')
q = SBString('hello world')
#q.insert(len(q.get_string()), 'z')

for r in range(replicates):
	t = random.randint(0, 1)
	if t > .5:
		code = 'i'
	else:
		code = 'd'
	if len(q) < 10:
		code = 'i'
	testblock(q, code, 3, txt=random_string(random.randint(1, 10)), del_count=random.randint(1, 4))

