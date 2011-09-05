# test if the state_id stays put when batch=true
from SBStrList import *

st = SBString('adf')
st.insert(1, 'Z', batch=True)
st.insert(1, 'Z', batch=True)
assert(st.get_state_id() == 0)


s = SBStrList(['a\n', 'bbb\n', 'cccc\n'])
s.insert(1, 'qq', batch=False)
s.insert(1, 'Z', batch=True)
s.insert(1, '9', batch=True)
assert(s[0].get_state_id() == 1)

s[0].get_string(state_id=2)
s[0].get_string(state_id=1)
