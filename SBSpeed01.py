# this tests some problems with sblist._get_l_idx,
# and requires some code inside the target programs
# like:
#   endt = datetime.datetime.now()
#    dprint('llen took ' + str((endt - startt).microseconds) )#
#
import datetime, time
from SBStrList01 import *

st = SBString('adf')
times = []
times.append( datetime.datetime.now())
for k in range(10):
	for j in range(10):
		junk = st.insert(1, 'a')
	times.append(datetime.datetime.now())

print('done')

print('incremental times in microseconds:')
for j in range(1, 10):
	print((times[j] - times[j - 1]).microseconds)


#for j in range(100):
#	junk = st.oncetest(j)
#times.append(datetime.datetime.now())
