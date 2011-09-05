from SBStrList import *

q = SBStrList(['abcdefg\n'])
q.insert(2, 'AAA\nBBBB')
repr(q[0])
assert(q[0].get_string() == 'abAAA\n')

q.insert(5, 'Z')
assert(q[0].get_string() == 'abAAAZ\n')



q = SBStrList(['abcdefg'])
q.insert(2, 'AAA\nBBBB')
repr(q[0])


q = SBStrList(['Edit this string\n', 'This is line2\n'])
q.show_line_pts()
q.insert(6, '\n')
q.show_line_pts()
repr(q[2])
