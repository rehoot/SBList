from SBList import *

import sys
print('------------------------------------------------------------')
print(sys.argv[0])

l = ['h', 'e', 'b', 'u', 's', 'p', 'x', 'a']
n = ['h', 'e', 'b', 'aaa', 's', 'p', 'x', 'a']
o = ['h', 'e', 'b', 'zzz', 's', 'p', 'x', 'a']

m = [4, 5, 7, 1, 33, 44, 22, 88, 54]

ql = SBList(l)
qn = SBList(n)
qo = SBList(o)
qm = SBList(m)

#print(repr(ql))
#ql.delete(2)
#ql.delete(2, batch=True)
#ql.delete(2, batch=True)
#print(repr(ql))
#ql.get_undo_list()
#raise Exception("temp stop")

assert(ql[3] == 'u')
assert(qm[1] == 5)
assert(ql[-1] == 'a')
assert(qm[-1] == 54)
assert(ql[2] + ql[4] == 'bs')
assert(qm[2] + qm[4] == 40)
assert('x' in ql)
assert(88 in m)
##print(ql[1:4])
assert(ql[1:4] == ['e', 'b', 'u'])

#
assert(l <= l)
assert(l >= l)
assert(n <= l)
assert(o >= l)
assert(o > l)
assert(l == l)
assert(l != m)
assert(l != o)
assert(l < o)
#

assert(ql <= ql)
assert(ql >= ql)
assert(qn <= ql)
assert(qo >= ql)
assert(ql == ql)
assert(ql != qm)
assert(ql != qo)
assert(qo > ql)
assert(ql < qo)
#

ql.insert(3, 'hello insert to 3')#
ql.insert(5, 'abcdefg insert to 5')
print("---------- test after 2 inserts:")
print('ql is ' + repr(ql) + ' state: ' + ql.show_state())

ql.delete(2)
print("---------- test after delete 2")
print('ql is ' + repr(ql) + ' state: ' + ql.show_state())


print("TESTING UNDO STATE: " )
ul = ql.get_undo_list()
for x in ul:
		print(repr(x))


ql.delete(2)
print("---------- test after second delete 2")
print('ql is ' + repr(ql) + ' state: ' + ql.show_state())

ql.insert(3, 'replaced to 3', batch=True)
print("---------- test after batch insert to idx 3:")
print('ql is ' + repr(ql) + ' state: ' + ql.show_state())

ql.insert(5, 'insert batch to 5', batch=True)
print("---------- test after batch insert:")
print('ql is ' + repr(ql) + ' state: ' + ql.show_state())


ql.delete(4, batch=True)
print("---------- test after batch delete from 4:")
print('ql is ' + repr(ql) + ' state: ' + ql.show_state())


ul = ql.get_undo_list()
for x in ul:
		print(repr(x))
#

print('finished OK')
