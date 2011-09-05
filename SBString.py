# SBString.py
# THIS PROGRAM HAS MANY BUGS, BUT MIGHT BE USEFUL TO SOMEBODY.
# THIS PROGRAM HAS MANY BUGS, BUT MIGHT BE USEFUL TO SOMEBODY.
# THIS PROGRAM HAS MANY BUGS, BUT MIGHT BE USEFUL TO SOMEBODY.

#format note: fix my programs:
# 1) add each sub-string to a list and ''.join() that list after the loop terminates.
# 2) import one per line and alphebetize
# SBString.py: a state-based, object-oriented string object
# that allows for easy undo processing but otherwise works
# like a regular python string.
########################################################################
# This file is part of the SBList collection of python scripts.
#
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License as published by the 
#Free Software Foundation version 3.
#
#This program is distributed in the hope that it will be useful, 
#but WITHOUT ANY WARRANTY; without even the implied warranty of 
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License 
#along with this program. If not, see <http://www.gnu.org/licenses/>.
########################################################################
#
# TO DO:
# * ADD A LIST OF COMMENTS TO SBSTRING KEYED BY ORIGINAL STORAGE ROW,
#   make it another SBSTring object with a possible note.
# * If new comment lines are inserted (modified from regular lines)
#   display them as regular lines located above whatever line below
#   it that is displayed. These will be stored as reguarl SBStrings
# * The 'hide comments' command will be a one-time pass to hide
#   existing comments, but it will not affect newly inserted comment lines.
#
# * ADD A SINGLE NOTE string TO EACH LINE
# * prevent deleting or moving comment lines when some levels of comments
#   are hidden (to avoid amibuous moves to new lines)
#
#
__author__ = "Robert E. Hoot (rehoot@yahoo.com)"
__version__ = "0.01"
__date__ = "$Date: 2011/04/20 $"
__copyright__ = "Copyright 2011, Robert E. Hoot"
__license__ = "GNU General Public License Version 3"


import datetime
import sys
from SBList import *

class VirtView():
	'''class VirtView()
	THIS SHOULD PROBABLY MOVE INSIDE SBSTRING OBJECT
	AND BE RENAMED.
 
	This object holds a list that contains abstracted
	pointers that allow for a logical view of the foreign
	text in an SBString object.  
	If edits are made to the foreign text, new text
	entries will be appened to the end of the foreign list but the pointers 
	here will be ordered so that the intended logical view
	of the foreign text is preserved.  

	Example: the foreign list contains the text "abcdefghij", then I 
	insert "zz" after "d", which is offset 4.  The new text ("zz")
	is appended to the end of the foreign list object
	but the entry in this object becomes:
	   [[0, 4, 0], [0, 2, 1], [4, 9, 0]]
	The entry for [0, 2, 1] means to grab bytes 0-1 (which
	is python slice s[0:2]) from the string that is stored
	at index 1 in the foreign list.
	
	*range* format: [start, end, list_offset_for_text]	
	where start and end* are python *slice()* numbers that
	point into the text that is referenced by the list offset.
	'''
	class StateEntry(object):
		start_pt = None
		end_pt = None
		list_idx = None
		length = None
		def __init__(self, start_pt, end_pt, list_idx):
			object.__init__(self)
			self.start_pt = start_pt
			self.end_pt = end_pt
			self.list_idx = list_idx 
			self.length = self.end_pt - self.start_pt
		def __repr__(self):
			return('[' + str(self.start_pt) + ', ' + str(self.end_pt) \
				+ ', '+ str(self.list_idx) + ', ' + str(self.length) + ']')

	class StateDeRef(object):
		'''class StateDeRef()
		This class will hold some values that will help to
		translate an entry in the state list to an entry
		in the main list.  

		The state list holds range entries with [start, end]
		indexes (in python slice() format) that refer to
		entries in the main list object.

		state_offset = the zero-based offset into the state
		               object.
		state_adj    = a virtual offset that would point to
		               a logical value in the range [start, end].
		               For example, if the state entry is [10, 20]
		               and state_adj = 3, then the reference is to
		               an entry in the main list at offset 13, which
		               is 10 + 3.
		list_idx     = an index into self.l that corresponds to
		               self.state[state_offset][0] + state_adj.
		'''

		state_offset = None
		state_adj = None
		str_ptr = None
		list_idx = None
		def __init__(self, s_offset, s_adj, str_ptr, l_idx):
			'''StateDeRef.__init()
			'''
			object.__init__(self)
			self.state_offset = s_offset
			self.state_adj = s_adj
			self.str_ptr = str_ptr
			self.list_idx = l_idx
		def __iter__ (self): 
			# Maybe add a flag that will lock the objects from
			# being altered when iter is active?
			self.iterindex = 4
			return(self)
		def __next__(self):
			self.iterindex -= 1
			if self.iterindex == 4:
				return(self.state_offset)
			elif self.iterindex == 3:
				return(self.state_adj)
			elif self.iterindex == 2:
				return(self.str_ptr)
			elif self.iterindex == 1:
				return(self.list_idx)
			else:
				raise StopIteration

		def __repr__(self):
			return([repr(self.state_offset) + ', ' + repr(self.state_adj) \
					+ repr(self.str_ptr) + repr(self.list_idx)])

	def __init__(self, state_entry):
		'''VirtView.__init__()
		'''
		self.state = SBList([state_entry])
		# use self.get_state_id()
		#self.state_id = 1 # NOT USED??

	def __iter__ (self): 
		# Maybe add a flag that will lock the objects from
		# being altered when iter is active?
		self.iterindex = len(self.state)
		return(self)

	def __getitem__(self, i):
		return(self.state[i])

	def __len__(self):
		'''VirtView.__len__()
		Returns the number of saved states.
		'''
		return(len(self.state))

	def __next__ (self): 
		'''VirtView.__next__
		Returns a range object, which contains
		a start offset, end offset, and an id for 
		a string stored elsewhere.  The start/end
		pair follows python slice() notation where
		end is one greater than the value that will
		be returned when used as list[start : end]
		'''
		# return an object of type xxx with each iteration.
		if self.iterindex == 0:
			raise StopIteration
		self.iterindex -= 1
		##(s_offset, s_adj, l_idx) = self._get_vl_idx(self.iterindex)
		##return(self.state[l_idx])
		return(self.state[len(self.state) - self.iterindex])

	def __repr__(self):
		return(repr(self.state))


	def _get_vl_idx(self, str_offset, state_id=-1):
		'''VirtView._get_vl_idx()
		Return pointers into state and a dereferenced
		pointer into the the foreign list for the given
		character offset.

		If the character offset is beyond the 
		virtual length of the underlying object, this
		returns [None, None, None, None], which might mean 
		to append a proposed insert at the end of the list.
		'''
		if state_id == -1: state_id = self.get_state_id()
		#assert(state_id < (len(self.state) ))
		str_len = self.get_llen(state_id=state_id)
		if str_offset >= str_len: #l_list_len:
			return([None, None, None, None])
		# temp_str_offset will be the starting offset into the string
		# in the range of pointers at this state offset.  If temp_str_offset
		# is less than the desired offset, read the next range of
		# pointers from this state and see if the span of that range
		# adds enough to temp_str_offset to contain the desired offset.
		temp_str_offset = 0	
		l_adjust = None
		#print('SBSTring. char offset=' + str(str_offset) +' state: ' + repr(self.state))
		for s_offset in range(len(self.state)):
			# For each s_offset in the current state (s_offset
			# is an index into character offset
			# ranges entered into the current state).
			#
			# 'highest_str_offset' is the highest character offset that would
			# be captured by the tuple in self.state[state_id][s_offset].
			highest_str_offset = temp_str_offset + self.state[s_offset].end_pt \
				- self.state[s_offset].start_pt - 1
			if highest_str_offset < str_offset:
				# We have not scanned forward far enough to reach the
				# desired virtual row, advance the search row index:
				temp_str_offset = highest_str_offset + 1
			else:
				# The desired string offset is in this range
				#
				# Within the specified range, I want to find the entry
				# in l that is 'offset' from the first entry in
				# the current range, so the real data will be in
				# l[state[state_id][0] + l_adjust]
				l_adjust = str_offset - temp_str_offset 

				temp_str_offset += l_adjust
				break
		# Return 
		# 1) s_offset = (state offset) an offset into the current state that contains
		#    a range that spans the specified virtual row.
		# 2) l_adjust = an offset that should be added to the contents of
		#    state[s_offset][0] to point into l to
		#    find the specifed virtual row; e.g.:
		#    l[self.state[s_offset][0] + l_adjust]
		# 3) l_offset = the desired string? offset into the text object?
		#  
		# I think str_pt is now used to point to the character offset within
		# a chunk of text, and string_id is the index of the list entry in
		# the foreign list.
		str_pt = self.state[s_offset].start_pt + l_adjust
		string_id = self.state[s_offset].list_idx 
		# IS STRING_ID THE SAME AS str_pt?
		# THIS ASSERTION FAILED: assert(string_id == str_pt)
		sd = self.StateDeRef(s_offset, l_adjust,  str_pt, string_id)
		return(sd)

	def delete_state(self, s_offset, batch=False, state_id=-1):
		'''VirtView.delete_state()
		Delete a *range* item from the state.
		'''
		if state_id == -1: state_id = self.get_state_id()
		#del self.state[s_offset]
		self.state.delete(s_offset, state_id=state_id, batch=batch)
		return(0)

	def get_item(self, idx, state_id=-1):
		if state_id == -1:
			state_id = self.get_state_id()
		return(self.state.get_item(idx, state_id))

	def get_list(self):
		return(self.state.return_list())
	
	def get_llen(self, state_id=-1):
		'''VirtView.get_llen()
		Return the length of the virtual string in the
		specified state.
		'''
		if state_id == -1: state_id = self.get_state_id()
		llen = 0
		#for s in self.state: ################################ THIS DIDN'T WORK
		startt =  datetime.datetime.now()
		#for j in range(len(self.state)):
		#	s = self.state[j]
		# The 'for s in self.state' version was 25% faster than for j in range(len(self.state
		# but is still slow. I then stored the list len in SBList and reduce run time by
		# half.
		for s in self.state:
			# Remember that the last index is in python format is
			# is one greater than the real index of what will
			# be includuded in this state element.
			#print('adding virtual len of state ' + repr(s) + ' totlen = ' + str(len(self.state)))
			#llen += s[1] - s[0]
			# The change from calculating length to storing made no difference
			llen += s.length
		endt = datetime.datetime.now()
		#dprint('llen took ' + str((endt - startt).microseconds) )#+ ' for loop count: ' + str(j))
		return(llen)

	def get_range(self, s_offset=-1, v_row=-1, state_id=-1):
		'''VirtView.get_range()
		Given either a state_offset or a virtual row index,
		return the *range* entry, which contains  
		start, end, string_id (where start and end are in
		python slice() format).

		You must pass a keyword argument for either s_offset
		or v_row.
		'''
		if state_id == -1: state_id = self.get_state_id()
		if s_offset == -1:
			if v_row == -1:
				raise Exception('You must pass either a state offset or a v_row " \
					+ "as a keyword parameter to get_range')
			else:
				#(s_offset, s_adj, l_idx, str_idx) = self._get_vl_idx(v_row)
				sd = self._get_vl_idx(v_row)
				return(self.state[sd.state_offset])
		else:
			return(self.state[s_offset])

	def get_state_id(self):
		'''VirtView.et_state_id()
		This gets the state ID from the underlying SBLIst object
		that holds the state information.

		see also self.state.incr_state_id()
		'''
		return(self.state.get_state_id())

	def insert(self, v_row, state_entry, state_id=-1, batch=False,):
		'''VirtView.insert()
		l_range is now a state_entry object

		*range* points to a slice of a foreign list, but
		the contents of that slice will be displayed 
		starting at the specified virtual row.

		I think *range* contains [start, end] but I'm not sure.
		
		Insert the range into the state list, and ideally
		I should merge state entries if the starting or ending
		values inside *range* are contiguous to those entries
		near it in the *state* list.
		'''
		times = []
		#dprint('-----------------insert start')
		if state_id == -1:
			state_id = self.get_state_id()
		v_idx = 0
		s_offset = 0
		# * a *range* is a 3-item list like [5, 8, 2], the fist two
		#            numbers of which are 
		#            a 'slice()' referece to a range of entries in 
		#            a foreign list object that can be identifed with the third nbr.
		# * s_offset points to an existing *range* entry in self.state
		# * sd.state_adj is an offset between l_range[0] and l_range[1]
		# * list_idx is an offset into the foreign table where the associated
		#            virtual item (v_row) is stored. Its value is between
		#            l_range[0] and l_range[1]
		#
		# Length of the string before insertion.
		times.append(['a', datetime.datetime.now()])	
		virtual_len = self.get_llen(state_id=state_id)
		times.append(['b', datetime.datetime.now()])	
		if virtual_len == 0:
			# The state list can be empty if the user deleted everything,
			# but point to row zero to facilitate insert()
			v_row = 0
		#print('vv, vrow = ' + str(v_row) + ' len ' + str(virtual_len) + ' state: ' + repr(self.state))
		if v_row >= virtual_len:
			# Append the new row at the end of self.state, regardless of how far 
			# v_row exceeds the length of self.state 
			self.state.append(state_entry, state_id=state_id, batch=batch)
			return(0)
		# For the given virtual row, find the index into self.state. I think
		# l_row is a character offset
		#(s_offset, s_adj, l_row, string_id) = self._get_vl_idx(v_row)
		sd = self._get_vl_idx(v_row)
		assert(sd.list_idx is not None)
		if sd.state_adj == 0:
			# The new *range* item belongs at the start of an existing range
			# so insert the new item here:
			times.append(['c', datetime.datetime.now()])
			self.state.insert(sd.state_offset, state_entry, state_id=state_id, batch=batch)
			times.append(['c2', datetime.datetime.now()])
		else:
			if self.state[sd.state_offset].end_pt == v_row:
				# The new item goes after this state entry
				times.append(['d', datetime.datetime.now()])
				self.state.insert(sd.state_offset + 1, state_entry, state_id=state_id, batch=batch)
				times.append(['d2', datetime.datetime.now()])
			else:
				# split the old range entry
				low = self.state[sd.state_offset].start_pt
				high = self.state[sd.state_offset].end_pt
				# I think str_id is an offset into the sblist for an immutable string.
				str_id = self.state[sd.state_offset].list_idx
				self.state.delete(sd.state_offset, state_id=state_id, batch=batch)
				# The deletion above should have creatd a new state for the self.state object.
				# I should now use that for the remainin transactions in this batch:
				state_id = self.state.get_state_id()
				# Insert the lower part of the state entry:
				times.append(['e', datetime.datetime.now()])
				self.state.insert(sd.state_offset, self.StateEntry(low, low + sd.state_adj, sd.list_idx), 
					batch=True, state_id=state_id)# batch is always true here
				# Insert the entry for the newly inserted text:
				self.state.insert(sd.state_offset + 1, state_entry, batch=True, state_id=state_id)
				# Insert the top half of the old range that was split
				self.state.insert(sd.state_offset+ 2, self.StateEntry(low + sd.state_adj, high, sd.list_idx), 
					batch=True, state_id=state_id)
				times.append(['e2', datetime.datetime.now()])
		#for j in range(1, len(times)):
		#	#dprint(times[j][0] + ', ' + times[j - 1][0] + ' ' 
		#	#	+ repr((times[j][1] - times[j - 1][1]).microseconds))
		return(0)


	def insert_state(self, s_offset, state_entry, state_id=-1, batch=False):
		'''VirtView.insert_state()
		Insert a range object into self.state.
		This is intended to facilitate rewriting
		the state for deletions in the virual
		representation of the underlyling list.
		see also: delete_state()
		'''
		if state_id == -1: state_id = self.get_state_id()
		self.state.insert(s_offset, state_entry, state_id=state_id, batch=batch)
		return(0)

	def set_state_id(self, id):
		self.state.set_state_id(id)
		return(0)
	
	def show_state(self, state_id):
		'''VirtView.show_state()
		return some debugging info
		'''
		#return(self.state.show_state(state_id=state_id))
		return(repr(self.state))
		
		
class SBString(object):
	class StateLog(object):
		state_id = None
		vstate_id = None
		prior_state_id = None
		def __init__(self, state_id, vstate_id, prior_state_id):
			object.__init__(self)
			self.state_id = state_id
			self.vstate_id = vstate_id
			self.prior_state_id = prior_state_id
		def __repr__(self):
			return('[' + str(self.state_id) + ', ' + str(self.vstate_id) + ', ' \
				+ str(self.prior_state_id) + ']')

	def __init__(self, txt, nickname=''):
		'''SBString.__init__()
		'''
		object.__init__(self)
		# The underlying list object begins as a list 
		# that contains only one string. Insertions of character
		# into the string will be appended to the end of self.l and
		# presented in the correct place in the virtual view.
		self.l = [txt]
		# nickname might be useful for debugging when you have many
		# instances of thie object
		self.buff_len = SBList([len(txt)])
		self.nickname = nickname
		# self.point will be keyed with self.state_id
		self.point = [0]
		self.state_id = 0
		# self.virtview holds pointers that allow me to reassemble
		# self.l into the intended text.
		self.virtview = VirtView(VirtView.StateEntry(0, len(txt), 0))
		# state_log saves all relevant state IDs (state ID for l is len-1):
		# main, view, prior
		# I think I need this because deletions affect only the *view*
		# object and inserts affect both *l* and *view*, and batch
		# changes can increment l and view without incrementing the main
		# state_id
		self.state_log = [self.StateLog(self.state_id, self.virtview.get_state_id(), -1)]
		assert(self.virtview.get_state_id() == self.state_id)

	def __len__(self):
		# REPLACE THIS TO USE THE STATIC BUFF_LEN OR STR_LEN() FUNCTIONS
		#return(len(self.get_string()))
		return(self.str_len())

	def __repr__(self):
		'''SBString.__repr__()
		Return a string representation of this object.
		'''
		return(self.get_string())

	def delete(self, start, count, batch=False, state_id=-1):
		'''SBString.delete()
		Delete the characters starting at *start* for
		*count* characters.
		'''
		# Note that the delete range might span more
		# than one text chunk and require redefining
		# two *range* values at the end points of the 
		# deletion zone.
		#
		# Function:
		# 1) find all of the entries in self.virtview
		#    that span the deletion zone.
		# 2) modify *range* values that are only partially
		#    in the deletion zone and delete others.
		# 3) do not delete any of the underlying text, because
		#    that will be retained internally for possible
		#    undeletion.
		end = start + count # end pt in python slice() format
		if state_id == -1:
			state_id = self.state_id

		s_len = len(self)
		if start >= s_len:
			return(0)
		if end > s_len:
			end = s_len
		del_len = end - start

		#(low_offset, low_adj, low_l_idx, string_id) = self.virtview._get_vl_idx(start)
		low = self.virtview._get_vl_idx(start)

		
		# WARNING, high.state_offset is not in slice() format to avoid pointing
		# to the next state offset, so I will try fudging the high.state_adj value
		# to restore it to slice() format.
		#(high_offset, high.state_adj, high_l_idx, string_id) \
		high	= self.virtview._get_vl_idx(end - 1)
		high.state_adj += 1
		#
		# get_range() now returns a StateEntry object
		low_range = self.virtview.get_range(s_offset=low.state_offset)
		high_range = self.virtview.get_range(s_offset=high.state_offset)
		incr_offset = 0
		batch_code = batch
		for j in range(low.state_offset, high.state_offset + 1):
			# Delete the state *range* stored at low.state_offset
			# and the higher states will fall into the slot
			# for the next deletion if needed.
			# Note: allow no more that one transaction to affect self.virtview.l.state_id
			# by making the first iteration use the orginal value of 'batch,' then
			# the other iterations using batch=True:
			self.virtview.delete_state(low.state_offset, batch=batch_code)	
			batch_code = True
	
		if high.state_offset > low.state_offset:
			# at least two of the old ranges were affected by the deletiong
			if low.state_adj == 0:
				# The entire first range was destroyed by the delete
				pass
			else:
				# Load a modified first range
				self.virtview.insert_state(low.state_offset, VirtView.StateEntry(low_range.start_pt, \
					low_range.start_pt + low.state_adj, low_range.list_idx), batch=True)
				incr_offset += 1

			#
			high_vrow = end - high.state_adj + (high_range.end_pt - high_range.start_pt)
			if high_vrow == end:
				# The entire seconde range was destroyed by the delete
				pass
			else:
				# load a modified second range:
				# (the incr_offset is an adjustment in case a prevous state range was
				# inserted above.
				self.virtview.insert_state(low.state_offset + incr_offset, \
					VirtView.StateEntry(high_range.start_pt + high.state_adj, high_range.end_pt, high_range.list_idx), \
					batch=True)
			
		else:
			# No more than one old range was affected by the deletion
			old_rng_len = low_range.end_pt - low_range.start_pt
			if del_len == old_rng_len:
				# the existing range object is the exact length of 
				# the deletion range, so don't restore it
				pass
			else:
				if low.state_adj == 0:
					# The character(s) that I want to delete is the first
					# in this range, so modify the range.
					self.virtview.insert_state(low.state_offset, VirtView.StateEntry(low_range.start_pt \
					+ low.state_adj + del_len, low_range.end_pt, low_range.list_idx), batch=True)
				else:
					# I have to split the range entry in half
					self.virtview.insert_state(low.state_offset, VirtView.StateEntry(low_range.start_pt, \
						low_range.start_pt + low.state_adj, low_range.list_idx))
					self.virtview.insert_state(low.state_offset + 1, VirtView.StateEntry(low_range.start_pt \
						+ low.state_adj + del_len, low_range.end_pt, low_range.list_idx), batch=True)
		# 
		# capture state_ids
		if not batch:
			# (end - start) reflects any error correction if the user tries to delete beynd EOL.
			self.incr_str_len(-1 * (end - start), state_id=self.state_id)
			self.incr_state_id()# This also rolls point to the new state
			# Save to sate log: current state,  viewstate, prior state
			self.state_log.append(self.StateLog(self.state_id, \
				self.virtview.get_state_id(), state_id))
		else:
			self.incr_str_len(-1 * (end - start), state_id=state_id)
			# Save to sate log: current state,  viewstate, prior state
			self.state_log[self.state_id] = self.StateLog(self.state_id, \
				self.virtview.get_state_id(), state_id)
		return(0)# end of delete

	def get_char(self, offset, state_id=-1):
		if state_id == -1:
			state_id = self.state_id
			vstate_id = self.virtview.get_state_id()
		else:	
			vstate_id = self.state_log[state_id].vstate_id
		idx = 0
		if offset >= len(self):
			return('')
		s = ''
		for j in range(len(self.virtview)):
			# v is a StateEntry object with start_pt, end_pt, list_idx...
			v = self.virtview.get_item(j, state_id=vstate_id)

			# Accumulate the count of characters that WILL have been
			# counted by the end of this chunk of text. Do this by
			# finding the difference between the 
			# starting and ending slice() indexes into this piece
			# of text:
			if (idx + v.length) > offset:
				start = offset - idx + v.start_pt 
				#s = self.l[v.list_idx][start: start+ 1]
				s = self.l[v.list_idx][start: start+ 1]
				dprint('found get_char: ' + repr( self.l[v.list_idx]) \
					+ ' offset = ' + str(offset) + ' vstar=' + str(v.start_pt)
					+ ' idx = ' + str(idx)
					+ ' start=' + str(start) + ' len=' + str(v.length))
				break
			idx += v.length
		return(s)
		
	def get_state_id(self):
		'''SBString.get_state_id()
		'''
		return(self.state_id)
	
	def get_string(self, state_id=-1):
		'''SBString.get_string()
		'''
		if state_id == -1:
			self.dump()
			vstate_id = self.state_log[-1].vstate_id
		else:	
			vstate_id = self.state_log[state_id].vstate_id
		tmp_l = [] 
		for j in range(len(self.virtview)):
			# v = self.virtview[j]
			v = self.virtview.get_item(j, state_id=vstate_id)
			#tmp_l.append(self.l[v[2]][v[0]:v[1]])
			tmp_l.append(self.l[v.list_idx][v.start_pt:v.end_pt])
		
		return(''.join(tmp_l))

	def get_point(self, state_id=-1):
		if state_id == -1:
			state_id = self.state_id
		#else:	
		return(self.point[state_id])

	def incr_point(self, incr, state_id=-1):
		"""SBString.incr_point()
		Let the editor call this, don't call it here

		Set the point to the specified value, but
		correct for errors if the value goes below
		zero or beyond EOL.

		"""
		if state_id == -1:
			state_id = self.state_id
		#else:	
		self.set_point(self.point[state_id] + incr)
		return(0)

	def incr_str_len(self, incr, state_id=-1):
		"""SBString.incr_str_len()
		Increment the stored value for the logical length of the string.
		This does not alter any state_id values.  When incr_point is
		called, that routine advances the buff_len to the next state.

		This was added for performance reasons because navigating the
		state list became slow after 100 edits. Storing this value
		in an SBList object allows for the length to be correct
		after undo() or redo() actions, but perhaps I could use a 
		regular list as was done with incr_point (if that works).
		"""
		if state_id == -1:
			state_id = self.state_id

		##self.set_point(self.point[state_id] + incr)
		self.buff_len.update(0, \
			self.buff_len[0] + incr, \
			state_id=state_id, batch=True) 	
		return(self.point[state_id])


	def incr_state_id(self):
		'''SBString.incr_state_id()
		Always use this to increment the state after a insert, delete
		or other such operation (in the future).
		This routine is needed to set the state_id properly after
		an undo is made.
		'''
		self.buff_len.append(self.buff_len[0])
		self.point.append(self.point[self.state_id])
		self.state_id = len(self.state_log) 
		return(0)
		
	def insert(self, start, txt, state_id=-1, batch=False):
		'''SBString.insert()
		'''
		if state_id == -1:
			save_state_id = self.state_id
			vstate_id = -1
		else:
			save_state_id = state_id
			vstate_id = self.state_log[state_id].vstate_id

		# New text is always appended to the end of self.l,
		self.l.append(txt)# Never use batch here.
		# ... but then the index from l is inserted into the 
		# logical view of the string:
		self.virtview.insert(start, VirtView.StateEntry(0, len(txt), len(self.l) - 1), \
			state_id=vstate_id, batch=batch)
		##### The point here is not used and is probably wrong !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		####self.point.append(self.point[save_state_id]) # Never use batch here.
		# capture state_ids
		if not batch:
			self.incr_state_id()
			#self.incr_point(len(txt), state_id=state_id)
			self.incr_str_len(len(txt), state_id=self.state_id)
			# Save to sate log: current state, lstate, viewstate, prior state
			self.state_log.append(self.StateLog(self.state_id, \
				self.virtview.get_state_id(), save_state_id))
		else:
			#self.incr_point(len(txt), state_id=state_id)
			self.incr_str_len(len(txt), state_id=state_id)
			# Save to sate log: current state, lstate, viewstate, prior state
			self.state_log[self.state_id] = self.StateLog(self.state_id, \
				self.virtview.get_state_id(), save_state_id)
		return(0)# end of insert()

	def set_point(self, pt, state_id=-1):
		if state_id == -1:
			state_id = self.state_id
		#else:	
		if pt > len(self):
			# apr 22, 00:004, was =lstate_id
			self.point[state_id] = self.str_len(state_id=state_id) - 1
		elif pt < 0:
			self.point[state_id] = 0
		else:
			self.point[state_id] = pt
		return(0)

	def show_state(self, state_id=-1):
		'''SBString.get_string()
		Return the set of *range* items that point to the 
		underlying strings.
		'''
		if state_id == -1:
			vstate_id = -1
		else:	
			vstate_id = self.state_log[state_id].vstate_id
		return('view state: ' + self.virtview.show_state(state_id=vstate_id))

	def str_len(self, state_id=-1):
		"""SBString.str_len()
		Return the length of the virtual string at the
		specified state ID (or current state if the state_id is
		not specified.
		"""
		###if state_id == -1:
		###	state_id = self.state_id
		#### was =lstate_id apr 22
		###return(len(self.get_string(state_id=state_id)))
		return(self.buff_len[0])

	def test_vl(self, str_offset):
		return(self.virtview._get_vl_idx(str_offset))

	def undo(self, count=1):
		"""SBString.undo()
		"""
		###self.state_id -= count
		##j = len(self.state_log) - 1
		##while j >= 0 and self.state_log[j - 1][0] == self.state_id:
		# Access the previous state id value from the log.
		# Remember that if the user used undo and then made edits,
		# the previous state value could point to nearly any of the valid states.
		self.state_id = self.state_log[-1].prior_state_id
		if self.state_id < 0:
			self.state_id = 0

		# Find the state IDs for the underlying list and the view-manager:
		vstate_id = self.state_log[self.state_id].vstate_id


		##self.l.set_state_id(lstate_id)
		self.virtview.set_state_id(vstate_id)
		return(self.state_id)
	def dump(self):
		return(0)
		print('-------------------------------------------------SBString Dump Start')
		print('state_id=' + str(self.state_id))
		print('point = ' + repr(self.point))
		print('bufflen ' + repr(self.buff_len))
		print('virtview ' + repr(self.virtview))
		print('log=' + repr(self.state_log))
		print('l ' + repr(self.l))

def dprint(msg):
	#pass
	print(msg, file=sys.stderr)

	
