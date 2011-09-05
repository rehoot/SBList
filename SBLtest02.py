from SBList import *
#####################################################################
#####################################################################
#
#                          Testing Insert
#
l = ['a', 'b', 'c', 'd', 'e', 'f']
q = SBList(l)	
print('Original: ' + repr(q))

q.insert(3, 'after c')
l.insert(3, 'after c')
#
## Validate _get_l_idx:
#for j in range(len(q)):
#	(s_offset, s_adj, l_idx) = q._get_l_idx_(j)
#	print("logical line" + str(j) + " s_offset" + str(s_offset) \
#  + " sadj " + str(s_adj) + " l idx:" + str(l_idx))

q.insert(7, "last line")
l.insert(7, "last line")
q.insert(7, "next to last line")
l.insert(7, "next to last line")
#print('q is ' + repr(q))
#print('l is ' + repr(l))
for j in range(len(l)):
	assert(q[j] == l[j])

revised = SBList(l)
assert(revised == q)
#######################################################################
#
#                      Testing Delete
#
print("--------------------------------------------------------")
l = ['a', 'b', 'c', 'd', 'e', 'f']
q = SBList(l)	
print('Original: ' + repr(q))

del q[5]
del q[4]
del q[0]
q.insert(2, 'after c')
q.insert(len(q), "last line")
del l[5]
del l[4]
del l[0]
l.insert(2, 'after c')
l.insert(len(q), "last line")
for j in range(len(l)):
	assert(q[j] == l[j])

revised = SBList(l)
assert(revised == q)

qlist = q.return_list()
assert(l == qlist)
print("delete last item, when last item is a single range  ")
q.delete(len(q) - 1)
print(repr(q))
print(q.show_state() + '\n')

######################## multiple delete:
#from SBList01 import *

l = ['a', 'b', 'c', 'd', 'e', 'f']
del l[1:3]
assert(l == ['a', 'd', 'e', 'f'])
assert(l != ['a junk list to be sure that the comparison works'])
del l[0:2]
assert(l == ['e', 'f'])
del l[1:2]
assert(l == ['e'])
del l[0:1]
assert(l == [])

#####################
print("------------------------------------------------")
print(" UPDATE TEST")
print("--------------------- - - - - - - - - - - - - - - -")
l = ['a', 'b', 'c', 'd', 'e', 'f']
q = SBList(l)	
print('Original: ' + repr(q))
for j in range(0, len(q)):
	q.update(j, 'new' + q[j])
	#print(q.show_state())
	#print(repr(q))
	#print("- - - - - - ")

q.update(len(q) - 1, 'new last row')
print(repr(q))
assert(repr(q) == '[newa, newb, newc, newd, newe, new last row]')
######################################################################
#
#
#
l = ['a', 'b', 'c', 'zz', 'd', 'e', 'f']
q = SBList(l)	
print('Original: ' + repr(q))

#l.insert(3, 'after c')
#q.insert(3, 'after c')

del l[2]
del q[2]

print('after del, q = ' + repr(q))
print('after del, l = ' + repr(l))

assert(l == q.return_list())
l.sort()
q.sort()

print('after sort, q = ' + repr(q))
print('after sort, l = ' + repr(l))

qlist = q.return_list()
assert(l == qlist)

print('sort after insert and delete')
print(repr(q.order()))

print("\nNow sort indexes 3-7")
print(repr(q.order(start=3, end=7)))

m = ['r', 'h', 'o', 's', 'u', 'sa', 'saa', 'm', 'o', 'sb', 'c']
q = SBList(m)	
print("\n\n****** list has been restored to\n" + repr(q))
q.sort()
print("\n**sorted list\n" + repr(q))
print(q.show_state())

m = ['r', 'h', 'o', 's', 'u', 'sa', 'saa', 'm', 'o', 'sb', 'c']
q = SBList(m)	
print("\n\n****** list has been restored to\n" + repr(q))
print(" sorting indices 3-7")
q.sort(start=3, end=7)
print(repr(q))
print(q.show_state())
