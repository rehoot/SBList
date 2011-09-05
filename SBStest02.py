from SBStrList import *
# validate some parts of SBStrList

####################
# 1) test get_string() and repr()
q = SBStrList(['hello there\n', 'line 2\n', 'this is line 3\n'])
assert(len(q[0]) == 12)
assert(q[0].str_len() == 12)
assert(q[0].get_string() == 'hello there\n')
assert(q[2].get_string() == 'this is line 3\n')
q.insert(6, 'ABC ')
len(q[0])
#for j in range(q.str_len()):
#	print('j ' + str(j) + ' line ' + str(q.pt_to_line(j)) + ' ' + q.get_char(j))
assert(q.pt_to_line(0) == 0)
assert(q.pt_to_line(15) == 0)
assert(q.pt_to_line(16) == 1)
assert(q.pt_to_line(22) == 1)
assert(q.pt_to_line(23) == 2)
assert(q.pt_to_line(37) == 2)

q.insert(18, ' TEST')
assert(repr(q) == 'hello ABC there\nli TESTne 2\nthis is line 3\n')
assert(q[0].get_string() == 'hello ABC there\n')
assert(q[2].get_string() == 'this is line 3\n')

q.delete(4, 3)
assert(repr(q) == 'hellBC there\nli TESTne 2\nthis is line 3\n')

print('q 0 len = ' + str(len(q[0])) + '  ' + repr(q[0]))
assert(q[0].str_len() == 13)
assert(q[2].str_len() == 15)

####################
# 3) pt_to_line
q = SBStrList(['hello there\n', 'line 2\n', 'this is line 3\n'])
assert(q.pt_to_line(0) == 0)
assert(q.pt_to_line(11) == 0)
assert(q.pt_to_line(12) == 1)
assert(q.pt_to_line(18) == 1)
assert(q.pt_to_line(19) == 2)

assert(q.pt_to_t_pt(0) == 0 )
assert(q.pt_to_t_pt(11) == 11 )
assert(q.pt_to_t_pt(12) == 0 )
assert(q.pt_to_t_pt(13) == 1 )
assert(q.pt_to_t_pt(18) == 6 )
assert(q.pt_to_t_pt(19) == 0 )
assert(q.pt_to_t_pt(20) == 1)

q.insert(23, 'XYZ')
q.insert(15, 'RST')
q.insert(6, 'PQR')
[len(q[0]), len(q[1]), len(q[2])]
q
q.delete(9, 2)
q.delete(32, 1)
assert(repr(q) == 'hello PQRere\nlinRSTe 2\nthisXYZ i line 3\n')
assert(q.pt_to_line(0) == 0)
assert(q.pt_to_line(12) == 0)
assert(q.pt_to_line(13) == 1)
assert(q.pt_to_line(22) == 1)
assert(q.pt_to_line(23) == 2)

assert(q.pt_to_t_pt(0) == 0 )
assert(q.pt_to_t_pt(12) == 12 )
assert(q.pt_to_t_pt(13) == 0 )
assert(q.pt_to_t_pt(14) == 1 )
assert(q.pt_to_t_pt(22) == 9 )
assert(q.pt_to_t_pt(23) == 0 )
assert(q.pt_to_t_pt(24) == 1)
####################
# from SBStrList01 import *
# 4) pt_to_line with batch=True
q = SBStrList(['hello there\n', 'line 2\n', 'this is line 3\n'])

q.insert(23, 'XYZ', batch=True)
q.insert(15, 'RST', batch=True)
q.insert(6, 'PQR', batch=True)
[len(q[0]), len(q[1]), len(q[2])]
q
q.delete(9, 2, batch=True)
q.delete(32, 1, batch=True)
assert(repr(q) == 'hello PQRere\nlinRSTe 2\nthisXYZ i line 3\n')
assert(q.pt_to_line(0) == 0)
assert(q.pt_to_line(12) == 0)
assert(q.pt_to_line(13) == 1)
assert(q.pt_to_line(22) == 1)
assert(q.pt_to_line(23) == 2)

assert(q.pt_to_t_pt(0) == 0 )
assert(q.pt_to_t_pt(12) == 12 )
assert(q.pt_to_t_pt(13) == 0 )
assert(q.pt_to_t_pt(14) == 1 )
assert(q.pt_to_t_pt(22) == 9 )
assert(q.pt_to_t_pt(23) == 0 )
assert(q.pt_to_t_pt(24) == 1)
####################
# from SBStrList01 import *
# 5) pt_to_line inserting into SBStri instead of SBStrList
q = SBStrList(['Line 001 1234567890\n', 'Line 002 1234567890\n', \
		'Line 003 1234567890\n'])

q.pt_to_line(19)
q.pt_to_line(20)
q.pt_to_line(25)
q.pt_to_t_pt(26)
q.pt_to_t_pt(70)

q[0].insert(5, 'ABCDE')
q.pt_to_line(19)
q.pt_to_line(20)
q.pt_to_line(25)
q.pt_to_t_pt(26)
q.pt_to_t_pt(70)
##################
q = SBStrList(['hello world\n', 'line 2\n', 'this is line 3\n'])
q.insert(6, 'there ')
len(q[0])
q.pt_to_line(18)
q.insert(18, ' TEST')
repr(q)
assert(repr(q) == 'hello there world\n TESTline 2\nthis is line 3\n')
##################
q = SBStrList(['hello world\n', 'line 2\n', 'this is line 3\n'])
q.insert(6, 'there ')
len(q[0])
q.pt_to_line(18)
q.insert(19, ' TEST')
repr(q)
assert(repr(q) == 'hello there world\nl TESTine 2\nthis is line 3\n')




##################
#from SBStrList01 import *
q = SBStrList(['hello world\n', 'line 2\n', 'this is line 3\n'])
q.delete(2, 1)
assert(repr(q) == 'helo world\nline 2\nthis is line 3\n')
q.delete(11, 3)
assert(repr(q) == 'helo world\ne 2\nthis is line 3\n')
q.delete(25, 2)
assert(repr(q) == 'helo world\ne 2\nthis is li 3\n')

#7#################
#from SBStrList01 import *
# validate some parts of SBStrList
q = SBStrList(['hello world\n', 'line 2\n', 'this is line 3\n'])

q.insert(9, 'QQQ')
q.insert(12, 'RRR')
q.insert(8, 'SSS')
q.delete( 4, 3)
q.insert(19, 'TTT')
q.insert(2, 'UUU')
q.show_undo_list()
q
#q.insert(25, 'NEW STUFF\nTHE OTHER LINE')
[len(q[0]), len(q[1]), len(q[2])]
q.insert(25, '1234567890\nABCDEFGHIJ')
[len(q[0]), len(q[1]), len(q[2]), len(q[3])]
repr(q[1])
q.insert(36, 'Z')
# The next assert tests update_line_pts when
# an insert is made to the first character on the 
# non-first line of the buffer
assert(repr(q[2]) == 'ZABCDEFGHIJine 2\n')

sb = SBList([])
sb.append(0)
sb.append(1)
sb.append(2)
sb.append(3)
assert(sb == [0,1,2,3])
#######################
#from SBStrList01 import *
q = SBStrList(['hello world\n', 'line 2\n', 'this is line 3\n'])
[len(q[0]), len(q[1]), len(q[2])]
repr(q[1])

q.insert(6, '\nNEW LINE')
