from SBList import *

# The first test will ensure that the append function works properly.
# A prior version would insert before the last entry instead of appending
sb = SBList([])
sb.append(0)
sb.append(1)
sb.append(2)
sb.append(3)
assert(sb == [0,1,2,3])
sb.insert(4, 4)
assert(sb == [0,1,2,3,4])
sb.insert(4, 3.5)
assert(sb == [0,1,2,3,3.5,4])
sb.insert(0, 0.5)
assert(sb == [0.5, 0,1,2,3,3.5,4])

# Test a simple undo and some insertions
sl = SBList([1,2,6,3,12,7])
sl.insert(2, 90)
sl.undo()
sl.insert(2, 90)
sl.insert(4, 50)
sl.insert(5, 9999999)
sl.insert(3, 20)
sl.delete(6)
sl.insert(3, 30)
sl
sl.sort()
sl
sl.delete(3)
assert(sl.get_list() == [1, 2, 3, 7, 12, 20, 30, 50, 90])
####

#######################################################################
# Test insert, sort, delete:
sl = SBList([1,2,6,3,12,7])
sl.sort()
sl.undo()
print('######## B')
print('answer should be:\n[1, 2, 6, 3, 12, 7]')
print(sl)

print('------------------------------------------')

sl = SBList([1,2,6,3,12,7])
sl.insert(2, 90)
sl.undo()
sl.insert(2, 90)
sl.insert(4, 50)
sl.insert(3, 20)
sl.insert(3, 30)
sl.sort()
assert(sl.get_list() == [1, 2, 3, 6, 7, 12, 20, 30, 50, 90])

sl.delete(3)
sl
assert(sl.get_list() == [1, 2, 3, 7, 12, 20, 30, 50, 90])
#print('state after delete 3 is: ' + sl.show_state())
#print('base list is ' + sl.show_l())
#print('answer should be:\n[1, 2, 3, 7, 12, 20, 30, 50, 90]')
#print(sl)
#print(repr(sl.order()))

############################
