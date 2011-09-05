# SBList.py
# THIS PROGRAM HAS MANY BUGS, BUT MIGHT BE USEFUL TO SOMEBODY.
#
# This program will define a list object called SBList that has 
# the functionality of a regular list object but internally it 
# is based on (mostly) immutable objects and will hopefully 
# allow undo operations without having to do any extra programming.
#
# The general idea is that each entry is stored and never deleted,
# and the data is presented in the desired order by keeping a 
# separate list with indexes to the appropriate item.
# Because every entry is saved in the (imitation) "read-only"
# storage area, I can perform "undo" operations by simply changing
# the master pointer to point to a prior state (which is just a
# list of pointers to the real data).
#
# Example 
# 
# 1) mylist = SBList(['a', 'b', 'c', 'd'])
#    internally:
#      SBList.l = ['a', 'b', 'c', 'd']
#      SBList.state_id will be set to zero
#      SBList.state = [[[0, 5]]]
#        ('state' is an list, that contains an list for each state.  Inside
#        the list for each state is a collection of 2-item lists that
#        represent the starting and ending indexes into SBList.l that should be
#        presented if the object is printed or accessed)
#      
# 2) mylist.insert(1, 'x')  --insert an 'x' before offset 1
#      SBList.l = ['a', 'b', 'c', 'd', 'x']  ('x' is stored at the end)
#      SBList.state_id will be incremented to 1
#      note: Remember that python slice notation starts at
#      zero and grabs up to but not including the last
#      entry, so SBList.l[1: 3] = ['b', 'c']
#      SBList.state = [
#                      [[0, 5]],   <<that is the old state
#                      [[0,1], [4, 5], [1, 4]]   <<this is the new state
#                     ]
#        state now contains three ranges in pything 'slice' notation
#        referring to entries in SBList.l.  The first says to take the
#        first entry in SBList.l, the next says to get item at offset 4,
#        and the last range says to get the items from offset 1 through
#        3 from SBList.l.
#      There is also a log in SBList.log
#      If you print the contents, it will be in the expected order:
#      a, x, b, c, d.
#
# 
# TODO
# 1) INSERTING TO AN EMPTY LIST FAILS!
# 2) __delitem_ is not ready
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
# Usage note:
# This generates a delete and an insert in two separate
# steps, as would be invoked by this:
#	 test = SBList([1,2,3])
#	 test[2] += 8
#
__author__ = "Robert E. Hoot (rehoot@yahoo.com)"
__version__ = "0.01"
__date__ = "$Date: 2011/04/20 $"
__copyright__ = "Copyright 2011, Robert E. Hoot"
__license__ = "GNU General Public License Version 3"
'''
static would mean that vbuff.vline_ptrs is saved for each state, but
the purpose of it is to linear, so either I don't make it static or
I rebuild the entire seq with every state, or i nest it within a
static state object that generalizes static oo.

point_start is currently inside vls, vl, and vc objects, but changes.
maybe it should be a static list, keyed for vls,

To compile

import py_compile
py_compile.compile('./SBList.py')

'''
import datetime
import os
import sys
#
#
#
class SBList():
	'''Class SBList
	State-Based, list-replacement object for sparcely
	populated lists. Provides undo feature.

	This object is intended to serve as a replacement for a
	regular list object but with the added advantage of 
	enabling undo. This version is intended to be used
	for nested objects that have undo.

	This object works by storing a list with immutable
	entries combined with an abstraction layer that allows
	for a logical view of the list that reflects insertions,
	deletions, and other changes.	This is achieved internally
	by appending all new list items to the end of the 
	a hidden list object and keeping a separate list object
	to keep a fresh set of indexes into the main list.

  One unique feature of this object is that some of the
  functions (like .insert() and .delete()) have optional
  arguments for state_id and batch code.  If batch code is
  True, then multiple edits will be squashed into one state
  change.	You might want to use this feature to save a global
  find/replace as one undo event.	To use this feature, call
  the first insert or delete action with batch=False (which
  invokes a new state), then call all the remaining
  transactions with batch=True.

	'''
	class StorageRef(object):
		storage_start = None
		storage_end = None
		logical_start = None
		logical_end = None
		def __init__(self, storage_range, logical_range):
			object.__init__(self)
			self.storage_start = storage_range[0]
			self.storage_end = storage_range[1]
			self.logical_start = logical_range[0]
			self.logical_end = logical_range[1]

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
		list_idx = None
		def __init__(self, s_offset, s_adj, l_idx):
			object.__init__(self)
			self.state_offset = s_offset
			self.state_adj = s_adj
			self.list_idx = l_idx
		def __iter__ (self): 
			'''StateDeRef.__iter__()
			'''
			# Maybe add a flag that will lock the objects from
			# being altered when iter is active?
			self.iterindex = 3
			return(self)
		def __next__(self):
			'''StateDeRef.__next__()
			'''
			self.iterindex -= 1
			if self.iterindex == 3:
				return(self.state_offset)
			elif self.iterindex == 2:
				return(self.state_adj)
			elif self.iterindex == 1:
				return(self.list_idx)
			else:
				raise StopIteration

	class Undo():
		'''class Undo()
		This class contains some information about one undo action.
		It contains:

		the old row index(zero-based)
		the old contents of that row
		the new contents of that row
		'''
		class UndoChanges():
			row_idx = None
			old = None
			new = None
			def __init__(self, row_idx, old, new):
				'''UndoChanges.__init__
				'''
				self.row_idx = row_idx
				self.old = old
				self.new = new
			def __repr__(self):
				'''UndoChanges.__repr__
				'''
				return(str(self.row_idx) + ', ' + str(self.old) +', ' + str(self.new))

		def __init__(self, action, state, row, old, new):
			'''Undo.__init__
			'''
			self.action_type = action
			self.state_id = state
			self.row_idx = row
			self.old = old
			self.new = new
			#self.changes = []
			#self.changes.append(self.UndoChanges(row, old, new))
		
		def __repr__(self):
			'''Undo.__repr__
			'''
			s = self.action_type + ', ' + str(self.state_id) + ', '
			s += str(self.row_idx)	+ ', ' + repr(self.old)	+ ', ' + repr(self.new)
			return('[' + s + ']')
	
		def __getitem__(self, x):
			'''Undo.__getitem__()
			'''
			# This returns an chunk from undo.
			# this is a bad idea, but I didn't want
			# to write the regular 'get' funcions
			if type(x) == type(slice(1,2)):
				temp = []
				if x.step is None:
					step = 1
				else:
					step = x.step
				for j in range(x.start, x.stop, step):
					temp.append(self.__getitem__(j))
				return(temp)
			else:
				if x == 1:
					return(self.action_type)
				if x == 2:
					return(self.state_id)
				if x == 3:
					return(self.row_idx)
				if x == 4:
					return(self.old)
				if x == 5:
					return(self.new)
				else:
					return(None)
	
		def __iter__ (self): 
			'''Undo.__iter__
			'''
			# Maybe add a flag that will lock the objects from
			# being altered when iter is active?
			self.iterindex = len(self)
			return(self)
			
		def get_action_code(self):
			'''Undo.get_action_code()
			This returns an action code like 'i' for insert or 'd' for delete.
			Change and replace actions might be represented by two entries:
			one deletion and one insert.
			'''
			return(self.action_code)
	
		def get_old(self):
			'''Undo.get_old()
			This returns the old value that was changed by an edit event.
			'''
			return(self.old)
	
		def get_new(self):
			'''Undo.get_new()
			This returns the new version of the list element after edits.
			'''
			return(self.new)
	
		def get_row_idx(self):
			'''Undo.get_row_idx()
			This returns the zero-based row index of the row that was changed
			by an edit event.
			'''
		def get_state_id(self):
			'''Undo.get_state_id()
			'''
			return(self.state_id)
	#
	#
	############################################################
	#
	# Begin the functions for SBList class
	def __add__(self, x, y):
		'''SBList.__add__()
		'''
		if type(x) == type(slice(1,2)):
			raise Exception("Do not pass a slice as a target of addition:" \
				+ repr(x))
		if len(self) == 0:
			return(None)
		if x > len(self):
			return(None)
		return(self.l[self.get_lrow_idx(x)] + self.l[self.get_lrow_idx(y)])

	def __contains(self, y):
		return(y in self.l)

	def __delitem__(self, x):
		if type(x) == type(slice(1,2)):
			temp = []
			# access the logical length of the virtual representation
			# of the list:
			if x.stop > self.get_llen():
				raise IndexError
			if x.step is None:
				step = 1
			else:
				step = x.step
			b_code = False
			for j in range(x.start, x.stop, step):
				self.delete(x, batch=b_code)
				b_code = True
			return(temp)
		else:
			self.delete(x)
		return(0)

	def __eq__(self, y):
		'''SBList.__eq__()
		This will compare the virtual view of the current
		list object to a foreigh list object.

		Warning. If you intend to use this to compare
		the current list to another list, review the
		treatment of what happens when the two lists have
		different lengths--modify if need be.
		'''
		if len(self) == 0:
			return(False)

		if len(y) != len(self):
			return(False)
		else:
			for j in range(len(self)):
				if self.l[self.get_lrow_idx(j)] != y[j]:
					return(False)
			return(True)

	def __ge__(self, y):
		'''SBList.__ge__()
		This will compare the virtual view of the current
		list object to a foreign list object.

		Warning. If you intend to use this to compare
		the current list to another list, review the
		treatment of what happens when the two lists have
		different lengths--modify if need be.
		'''
		if len(self) == 0:
			return(False)

		if len(y) != len(self):
			return(False)
		else:
			for j in range(len(self)):
				if self.l[self.get_lrow_idx(j)] < y[j]:
					return(False)
			return(True)
		
	def __getitem__(self, x):
		'''SBList.__getitem__()
		Return an item from the list when accessed like l[x],
		where x is the row index of the logical represetation
		of the list.
		'''
		# This returns an item from the main list based
		# on the virtual row index, *x*.	That index
		# can be a slice(), which is a range() specifed
		# in python format (i.e., the last index is one
		# greater than what you want returned).
		if len(self) == 0:
			return(None)

		if type(x) == type(slice(1,2)):
			temp = []
			#if x.stop > len(self.l):
			if x.stop > self.get_llen():
				raise IndexError
			if x.step is None:
				step = 1
			else:
				step = x.step
			for j in range(x.start, x.stop, step):
				temp.append(self.l[self.get_lrow_idx(j)])
			return(temp)
		else:
			## self.get_item will perform the check on llen
			#if x >= self.get_llen():
			#	raise IndexError
			return(self.get_item(x, state_id=self.state_id))

	def __gt__(self, y):
		'''SBList.__gt__()
		This will compare the virtual view of the current
		list object to a foreign list object.

		Warning. If you intend to use this to compare
		the current list to another list, review the
		treatment of what happens when the two lists have
		different lengths--modify if need be.
		'''
		# Two lists can have the first n elements
		# the same and then when the first difference
		# is detected, the calculation can be determined
		# and the loop can be quit using a direct return().
		if len(self) == 0:
			return(None)

		if len(y) != len(self):
			return(False)
		else:
			for j in range(len(self)):
				if self.l[self.get_lrow_idx(j)] > y[j]:
					#gt_proved = True
					return(True)
				elif self.l[self.get_lrow_idx(j)] < y[j]:
					return(False)
			# The lists were identical, so return false
			return(False)
		

	def __init__(self, lst, nickname=''):
		'''SBList.__init__()
		'''
		#### WHAT WOULD MAKE THIS METHOD EASIER TO OVERRIDE
		#### FOR USERS THAT INVENT THEIR OWN OBJECT TYPE
    #### THAT IS PASSED TO THIS???
		#### MAYBE THEY WOULD NEED TO CAST THE INPUT LIST SO
		#### THAT THE ITEMS ARE ALREADY OF THE CORRECT TYPE?
		
		# Copy the list line by line or else changes in
		# the original list will be passed into this object by
		# mistake
		self.l = [None] * len(lst)
		# nickname might be useful for debugging when you have many
		# instances of this object.
		self.buff_len = [len(lst)]
		self.nickname = nickname
		for j in range(len(lst)):
			self.l[j] = lst[j]
		self.state_id = 0
			
		# self.state contains lists. Each list contains
		# one or more range entries that contain starting and 
		# ending indexes into self.l that can be used to reconstruct 
		# the virtual view of the list. 
		# [[start, end], [start, end] ...]
		self.state = [[[0, len(lst)]]]
		# The log list will contain a list for each edit: 
		# [prior_state_id, edit_code, row_idx], with
		# codes being 'i' = insert, 'd' = delete.
		# The log enables the undo function to identify
		# what the prior state was, which can be tricky if there
		# have been edits after an undo.
		# Note that the log is a regular list and will show transactions
		# even after they have been undone.
		self.log = []
		self.prior_state_id = 0

	def __iter__ (self): 
		'''SBList.__iter__()
		'''
		# Maybe add a flag that will lock the objects from
		# being altered when iter is active?
		#
		# Note that I cannot use the length of self.l because
		# it might contain records for items that where since
		# deleted or removed via undo(). Use self.get_llen to
		# get the logical length of the virtual represenation of
		# the list.
		self.iterindex = self.get_llen()
		return(self)

	def __le__(self, y):
		'''__le__
		This will compare the virtual view of the current
		list object to a foreign list object.

		Warning. If you intend to use this to compare
		the current list to another list, review the
		treatment of what happens when the two lists have
		different lengths--modify if need be.
		'''
		if len(self) == 0:
			return(False)

		if len(y) != len(self):
			return(False)
		else:
			for j in range(len(self)):
				if self.l[self.get_lrow_idx(j)] > y[j]:
					return(False)
			return(True)
		

	def __len__(self):
		'''SBList.__len__()
		Returns the length of the virtual list object.
		'''
		return(self.get_llen(state_id=self.state_id))

	def __lt__(self, y):
		'''__lt__
		This will compare the virtual view of the current
		list object to a foreign list object.

		Warning. If you intend to use this to compare
		the current list to another list, review the
		treatment of what happens when the two lists have
		different lengths--modify if need be.
		'''
		if len(self) == 0:
			return(False)

		if len(y) != len(self):
			return(False)
		else:
			for j in range(len(self)):
				if self.l[self.get_lrow_idx(j)] < y[j]:
					return(True)
				elif self.l[self.get_lrow_idx(j)] > y[j]:
					return(False)
			return(False)
		
	def __ne__(self, y):
		'''__ne__
		This will compare the virtual view of the current
		list object to a foreign list object.

		Warning. If you intend to use this to compare
		the current list to another list, review the
		treatment of what happens when the two lists have
		different lengths--modify this functions if need be.
		'''
		if len(self) == 0:
			return(False)

		if len(y) != len(self):
			return(True)
		else:
			diff_found = False
			for j in range(len(self)):
				if self.l[self.get_lrow_idx(j)] !=	y[j]:
					diff_found = True
			return(diff_found)

	def __next__ (self): 
		'''SBList.__next__()
		Return a list entry with each call.
		'''
		assert(len(self.state) != 0)
		self.iterindex -= 1
		if self.iterindex < 0:
			raise StopIteration
		#
		# the countdown starts at the maximum value, but I want
		# to reverse the index to start at zero:
		new_idx = self.get_llen() - self.iterindex - 1
		sd = self._get_l_idx(new_idx)
		if sd.list_idx is None:
			raise StopIteration
		return(self.l[sd.list_idx])

	def __repr__(self):
		'''SBList.__repr__()
		Return a string representation of this object.
		'''
		#s = ''
		tmp_l = []
		for m in self.state[self.state_id]:
			for n in range(m[0], m[1]):
				#if s != '':
				#	s += ', ' #os.linesep 
				#s += str(self.l[n])
				tmp_l.append(str(self.l[n]))
		return('[' + ', '.join(tmp_l) + ']')

	def __setitem__(self, i, y):
		self.update(i, y)
		return(0)

	def _get_l_idx(self, v_row, state_id=-1):
		'''SBList._get_l_idx()
		Find an offset into the underlying list for the specified
		virtual row index (where virtual row index is a virtual 
		row index and both v_row and return are zero-based
		indexes).
	
		WARNING. This will return None in the l_idx slot if the
		state list is empty.	This can happen if the user deletes
		everything.	Check the return code from this method or
		check the length of the state list to avoid a fatal exception.

		WARNING: This will return the index of the last item if the 
		user requests a row index that is beyond the length of the 
		list.

		USE PREFIX 'V' FOR 'VIRTUAL ROW' AND PREFIXT 'L' FOR THE
		'UNDERLYING LIST' INDEX.

		I NEED TO DECIDE IF I WANT THIS TO FAIL WHEN THE V_ROW
		VALUE IS TOO HIGH. I THE PROBLEM IS RELATED TO THE NEED
		TO "INSERT" NEW ROWS AT THE END OF THE virtual LIST.
		'''
		if state_id == -1: state_id = self.state_id
		assert(state_id < (len(self.state) ))
		l_list_lenX = self.get_llen(state_id=state_id)
		if v_row >= l_list_lenX:
			v_row = l_list_lenX - 1
		# temp_vrow will be the starting virtual row (v_row) of the
		# range of pointers at this state offset.	If temp_vrow
		# is less than the desired v_row, read the next range of
		# pointers from this state and see if the span of that range
		# adds enough to temp_vrow to contain the desired v_row.
		temp_vrow = 0	
		l_adjust = None

		state_len = len(self.state[state_id])	
		assert(state_len >= 0 )
		startt = datetime.datetime.now()
		for s_offset in range(state_len):
			# For each s_offset in the current state (s_offset
			# is an index into
			# ranges entered into the current state).
			#
			# Remember that the list referenced by self.state[state_id]
			# is a list of start/end pointers into l. Note that l
			# will not be in virtual order after the first insert, so
			# we infer the virtual row of the modified l by counting 
			# the number of lines referenced by start/end pairs in
			# self.state[state_id].
			#
			# 'highest_vrow' is the highest virtual row that would
			# be captured by the tuple in self.state[state_id][s_offset],
			# remembering that python gets n-1 of the last index.
			highest_vrow = temp_vrow + self.state[state_id][s_offset][1] \
				- self.state[state_id][s_offset][0] - 1
			if highest_vrow < v_row:
				# We have not scanned forward far enough to reach the
				# desired virtual row, advance the search row index:
				temp_vrow = highest_vrow + 1
			else:
				# The desired v_row is in this range
				#
				# Within the specified range, I want to find the entry
				# in l that is 'offset' from the first entry in
				# the current range, so the real data will be in
				# l[state[state_id][0] + l_adjust]
				l_adjust = v_row - temp_vrow 

				temp_vrow += l_adjust
				break
		endt = datetime.datetime.now()
		dprint('_get_l_idx took ' + str((endt - startt).microseconds) )#
		# Return 
		# 1) s_offset = an offset into the current state that contains
		#		a range that spans the specified virtual row.
		# 2) l_adjust = an offset that should be added to the contents of
		#		state[state_id][s_offset][0] to point into l to
		#		find the specifed virtual row; e.g.:
		#		l[state[state_id][s_offset][0] + l_adjust]
		# 3) sd.list_idx = the desired offset into l that contains
		#		the specified virtual row.
		#	
		if state_len == 0:
			# The state list can be empty if the user deleted everything,
			# and some of my processes elsewhere regulararly delete and rebuild
			# the list, so it is not an error.
			l_idx = None
			s_offset = 0
			l_adjust = 0
		else:
			l_idx = self.state[state_id][s_offset][0] + l_adjust
		# Warning, test for l_idx being None in the event that the
		# state is empty due to deletions
		sd = self.StateDeRef(s_offset, l_adjust, l_idx)
		return(sd)
		
	def get_list(self):
		return(self.return_list())

	def get_state_with_vrows(self, state_list=None,	state_id=-1):
		'''SBList.get_state_with_vrows()
		loop through state and return
		a l-range and v-range, where the vrange
		is the python() slice representation of
		the virtual rows that are represented by
		the l-range item.
		'''

		temp_l = []
		if state_id == -1: state_id = self.state_id

		if state_list is None:
			state_list = self.state[state_id]

		temp_vrow = 0
		#for s in self.state[state_id]:
		for s in state_list:
			v_low = temp_vrow
			v_high = v_low + s[1] - s[0]
			temp_l.append(self.StorageRef(s, [v_low, v_high]))
			temp_vrow = v_high #apr 25 00:23
		return(temp_l)	
			
	def delete(self, v_row, state_id=-1, batch=False):
		'''SBList.delete()
		THE STATES HERE APPEAR TO BE WRONG.  IF AN OLD STATE 
		WAS SPECIFIED AS AN ARG, AND IF BATCH IS TRUE, THEN I
		NEVER WANT TO REFERENCE SELF.STATE!

		Remove the object at the specified virtual row index
		in sepcified state, then roll to a new state in which
		that item does not exist.

		Return the new state_id that does not contain the
		specified item.

		IF BATCH IS TRUE, THEN APPLY THE CHANGES AND RECORD
		THEM IN THE CURRENT STATE. THIS IS A WAY TO GROUP
		CHANGES SUCH AS WHEN APPLYING A GLOBAL SEARCH AND REPLACE.

		When using the *batch* flag, run the first insert or delete
		with batch=False, then apply all remaining changes with
		batch=True.
		'''
		max_srows = self.get_max_srows()
		# len_self is the length of the virtual list object
		len_self = len(self)
		if v_row > len_self:
			v_row = len_self
		if state_id == -1: state_id = self.state_id

		# find the offset into self.l that contains the deletion row,
		# and put that into sd.list_idx
		sd = self._get_l_idx(v_row, state_id=state_id)
		if sd.list_idx is None:
			# sd.list_idx will be None if self.state is empty
			assert(1==2)
			return(0)

		if not batch:	
			# point to the new state ID
			self.set_prior_state_id(self.state_id)
			# note that incr_state_id also appends a blank state
			self.incr_state_id()
			new_state_id = self.state_id
		else:
			new_state_id = state_id

		# *save_state* will be accessed below as the 'old' state.
		# It might be a snapshot of the current state before
		# batch changes are overlaid.
		save_state = []
		save_state.extend(self.state[state_id])

		if batch:
			# Clear the old/source state for batch/overlay
			# mode, and it will be recaptured from
			# the saved version
			self.state[state_id] = []

		temp_l = self.get_state_with_vrows(state_list=save_state, 
			state_id=state_id)
		for storage_ref in temp_l:
			# 'storage_ref' contains [[l_start, l_end], [v_row_start, v_row_end]]
			if storage_ref.logical_end <= v_row \
			or storage_ref.logical_start > v_row:
				# This range item in self.state does not contain the 
				# target deletion row, so add it to the new state:
				#self.state[self.state_id].append([storage_ref.storage_start, \
				#	storage_ref.storage_end])
				self.state[new_state_id].append([storage_ref.storage_start, \
					storage_ref.storage_end])
			#elif storage_ref[1][0] == v_row and (storage_ref[1][1] - 1) == v_row:
			elif storage_ref.logical_start == v_row \
			and (storage_ref.logical_end - 1) == v_row:
				# This range item in self.state is a range that exactly
				# equals the target delete row, so don't add it to the 
				# new state (thereby deleting it from the virtual view).
				# print('sblist deleting by omission')
				pass
			#elif storage_ref[1][0] == v_row:
			elif storage_ref.logical_start == v_row:
				# keep only the top part of this range
				#self.state[self.state_id].append([sd.list_idx + 1, \
				#	storage_ref.storage_end])
				self.state[new_state_id].append([sd.list_idx + 1, \
					storage_ref.storage_end])
			#elif (storage_ref[1][1] - 1) > v_row:
			elif (storage_ref.logical_end - 1) > v_row:
				# split the source range to represent the deletion
				self.state[new_state_id].append([storage_ref.storage_start, 
					sd.list_idx])
				self.state[new_state_id].append([sd.list_idx + 1, \
					storage_ref.storage_end])
			else:
				# the target is at the top of the range, so append only
				# the bottom of the source range
				self.state[new_state_id].append([storage_ref.storage_start, 
					sd.list_idx])
		if batch:
			self.log.append([self.get_prior_state_id(), 'd', v_row, new_state_id])
		else:
			self.log.append([state_id, 'd', v_row, new_state_id])

		#print('final state with vrows ' + repr(self.get_state_with_vrows()))
		self.buff_len[new_state_id] -= 1
		return(new_state_id)

	def append(self, item, batch=False, state_id=-1):
		self.insert(len(self.l), item, batch, state_id)
		return(0)

	def incr_state_id(self):
		'''SBList.incr_state_id()
		Create a new state and set self.state_id to it.
		Always use this to get a new state_id so that 
		everything works after an undo.
		'''
		# Advance the buffer len to the next state
		self.buff_len.append(self.buff_len[self.state_id])

		self.state_id = len(self.state) # Do this before appending
		self.state.append([])
		return(0)

	def insert(self, before_vrow, lst, batch=False, state_id=-1):
		'''SBList.insert()
		Insert the specified list object into the virtual
		representation of the underlying list, and return
		the new state_id.
	
		IF BATCH IS TRUE, THEN APPLY THE CHANGES AND RECORD
		THEM IN THE CURRENT STATE. THIS IS A WAY TO GROUP
		CHANGES SUCH AS WHEN APPLYING A GLOBAL SEARCH AND REPLACE.

		When using the *batch* flag, run the first insert or delete
		with batch=False, then apply all remaining changes with
		batch=True.
		'''
		# 0) Accumulate some values that will be needed later
		# 1) Scan self.state to find the state entry where the new row would
		# be.  
		# 2) Append start/end ranges from the old state into the new
		# self.state until we reach the desired row.
		# 3) Split the old range in self.state if needed.
		# 4) Finish appending the old pointers to the current state
		#		from the prior state.
		#
		#
		
		# 0) Accumulate some values that will be needed later
		append_flag = False
		new_l_idx = len(self.l)
		self.l.append(lst)
		len_self = len(self)
		max_srows = self.get_max_srows()
		if before_vrow >= len_self:
			# WARNING, THIS OVERRIDE MIGHT CAUSE CONFUSION OR SERIOUS PROBLEMS.
			# MAYBE I SHOULD RAISE AN EXEPTION OR CALL self.append()
			#raise Exception ("index for insertion is too high.  maybe use append.")
			append_flag = True
			before_vrow = len_self
		# 'state_id' is the prior state (which could be any prior state
		# if the user is trying to recover from bad edits).
		# self.state_id will become the new state that reflects the insertion.
		if state_id == -1: state_id = self.state_id
		#
		#
		# 1) Scan self.state to find the state entry where the new row would
		# be.  Note that some processes require that I clear the delete all
		# list elements, so an empty state or empty list is not an error.
		sd = self._get_l_idx(before_vrow, state_id=state_id)

		if sd.list_idx is None:
			# l_offset will be None if self.state is empty, which will happen
			# frequently when I delete all items in a 'state' list as I do in
			# SBString.
			# In this case, I want to insert to l_offset = 0.
			if sd.state_offset == 0:
				sd.list_idx = 0
			else:
				assert(2 == 3)
				pass
		#
		# I now have indexes into state and l, so I can build
		# the new state
	
		if not batch:
			# Save the old state ID for later use and keep it across transactions
			# that are in batch mode. 
			# Note that we cannot assume that the prior state is one less than 
			# the current state ID due to undo followed by edits.
			self.set_prior_state_id(state_id)
			# Create the new state and set self.state_id to it:
			self.incr_state_id()

		# *save_state* will be accessed below as the 'old' state.
		# It might be a snapshot of the current state before
		# batch changes are overlaid.
		save_state = []
		save_state.extend(self.state[state_id])
		if batch:
			# Clear the current state for batch/overlay
			# mode, and it will be recaptured from
			# the saved version
			self.state[state_id] = []

		temp_vrow = 0
		# k is the numeric value of the magic index into the OLD stat
		# i.e., the index corresponding to s in 'for s in save_state'
		k = 0
		if len(save_state) == 0:
			# This runs for only the initial load of the list.
			# Remember that self.state_id points to the new state.
			self.state[self.state_id].append([new_l_idx, new_l_idx + 1])
		else:
			for s in save_state:
				# For each entry in the old state,
				# append it to the new state or append modified
				# entries to account for the insertion:
				if k != sd.state_offset:
					# The index of s in self.state is not the index of the
					# state-entry that spans across the target insertion row.
					self.state[self.state_id].append(s)
				else:
					if temp_vrow == before_vrow:
						# If the current index range starts with
						# before_vrow, insert a range now:
						# Note that the ending virtual row of one range will 
						# often equal the begining range of another entry, but
						# the entry at the end is not included in the 
						# the real list due to python's format of list subscripts.
						self.state[self.state_id].append([new_l_idx, new_l_idx + 1])
						#
						if batch:
							self.log.append([self.get_prior_state_id(), 'i', temp_vrow, \
								self.state_id])
						else:
							self.log.append([state_id, 'i', temp_vrow, self.state_id])
						self.state[self.state_id].append(s)
					elif k == (max_srows - 1) \
					and (temp_vrow + s[1] - s[0]) == before_vrow:
						# The specified virtual row implies appending
						# the virtual row at the end of this range
						self.state[self.state_id].append([s[0], s[1]])
						self.state[self.state_id].append([new_l_idx, new_l_idx + 1])
						#
						if batch:
							self.log.append([self.get_prior_state_id(), 'i', temp_vrow + s[1], \
								self.state_id])
						else:
							self.log.append([state_id, 'i', temp_vrow + s[1], self.state_id])
					else:
						# I need to split the current range to insert
						# a link to the new value of l
						if append_flag:
							# append the record at the end of the existing ranges
							self.state[self.state_id].append([s[0], s[1]] )
							self.state[self.state_id].append([new_l_idx, new_l_idx + 1])
						else:
							self.state[self.state_id].append([s[0], s[0] + sd.state_adj] )
							self.state[self.state_id].append([new_l_idx, new_l_idx + 1])
						#
						if batch:
							self.log.append([state_id, 'i', temp_vrow + sd.state_adj, 
								self.state_id])
						else:
							self.log.append([self.get_prior_state_id(), 'i', temp_vrow \
								+ sd.state_adj, self.state_id])
						# append the second part of the split entry
						if not append_flag:
							self.state[self.state_id].append([s[0] + sd.state_adj, s[1]])
				k += 1
				temp_vrow += s[1] - s[0]
		self.buff_len[self.state_id] += 1
		return(self.state_id)
						
		
	def get_item(self, idx, state_id=-1):
		'''SBList.get_item()
		This will return the list item from the specified virtual
		row index.	Note that if you want to access the most
		recent state, you can use list notation like l[123]
		to get the item at index 123. The get_item() function
		allows the user to get a value from the virtual row index
		of a prior state.
		'''
		if state_id == -1: state_id = self.state_id
		assert(state_id < (len(self.state) ))
		llen = self.get_llen(state_id=state_id)
		#print('sblist getting item ' + repr(idx))
		if type(idx) == type(slice(1,2)):
			temp = []
			if idx.step is None:
				step = 1
			else:
				step = idx.step
			for j in range(idx.start, idx.stop, step):
				temp.append(self.l[self.get_lrow_idx(j, state_id=self.state_id)])
			return(temp)
		else:
			#if idx >= len(self.l):
			if idx == llen:
				# ttemp testingtemp testingtemp testingtemp testingtemp 
				raise IndexError
			if idx >= llen:
				raise IndexError
			tmp_idx = self.get_lrow_idx(idx, state_id=state_id)
			return(self.l[tmp_idx])

	def get_llen(self, state_id=-1):
		'''SBList.get_llen()
		Return the number of logical lines in the virtual list in the
		specified state.
		'''
		if state_id == -1: state_id = self.state_id
		###llen = 0
		####for s in self.state[state_id]:
		###for j in range(len(self.state[state_id])):
		###	s = self.state[state_id][j] #state is a regular list here
		###	# For each of the [start, end] range entries
		###	# in self.state, count the implied number of logical lines
		###	# in the list.
		###	# Remember that the last index is in python format is
		###	# is one greater than the real index of what will
		###	# be includuded in this state element.
		###	llen += s[1] - s[0]
		###return(llen)
		return(self.buff_len[state_id])

	def get_max_srows(self, state_id=-1):
		'''Return the number of entries in the current state.
		Each entry represents a range of index into the main
		list object such that the running total of values spanned
		by the ranges corresponds to the virtual display row
		of the virtual image of the data.

		When this object is first created, the return value should 
		be 1, representing the first and last python index
		values for the list.	If there are many changes
		to the list after intitialization, the number of state
		entries can be very high (and you might want to save
		and reload the buffer).
		'''
		if state_id == -1: state_id = self.state_id
		return(len(self.state[state_id]))

	def get_lrow_idx(self, v_row, state_id=-1):
		'''SBList.get_lrow_idx()
		Returns a zero-based index into the underlying list
		so that internal functions can point to the right
		item in the underlying list to retrieve the item at the
		specified virtual row.

		WARNING: THIS WILL RETURN None IF SELF.STATE IS EMPTY,
		SO ALWAYS CHECK THE RETURN CODE.

		WARNING: This method calls _get_l_idx, which will point
		to the last valid row if the user requests a row index
		that is beyond the list length.
		'''
		if state_id == -1: state_id = self.state_id
		# start with a linear search, optimize later
		assert(state_id < (len(self.state) ))
		sd = self._get_l_idx(v_row, state_id=state_id)
		return(sd.list_idx)

	def get_prior_state_id(self):
		return(self.prior_state_id)

	def get_state_id(self, offset=0):
		'''SBList.get_state_id()
		Returns the current state_id or 
		the state_id that associated with the
		specified index (preferably a negative
		integer that would represent number
		of states before the current one).
		
		Returns 0 if the offset is out of bounds
		(where zero should be the initial state).
		'''
		if abs(offset) > len(self.log):
			return(0)
		return(self.state_id + offset)

	def get_undo_list(self):
		'''SBList.get_undo_list()
		Return the list of Undo objects, which contains:
		1) either 'd' or 'i' (for delete or insert),
		2) the state_id into which an insert was made,
		or the state_id from which an item was deleted
		(i.e., the 'before' state_id), and
		3) the virtual row index for where the change occurred,
		4) the 'old' item, and
		5) the 'new' item (or None for delete).
		
		After I create the multi_insert and multi_delete
		funcitons, the list in number 3 above might contain a 
		batch of changes (such as the results of a global 
		change of text).
		'''
		temp = []
		for j in range(len(self.log)):
			old_state = self.log[j][0]
			action = self.log[j][1]
			v_idx = self.log[j][2]
			new_state = self.log[j][3]
			if action == 'i':
				old = None
				# SELF.LOG NEEDS A BATCH CODE OR THE NEW STATE_ID
				new = self.get_item(v_idx, state_id=new_state)
			else:
				old = self.get_item(v_idx, state_id=old_state)
				new = None
			# ADD CODE FOR 'U' AND MULTI-INSERT AND MULIT_DELETE !!!!!!!!!!!!!!!!!!!!!!
			
			temp.append(self.Undo(action, old_state, v_idx, old, new))
		return(temp)

	def order(self,	start=0, end=0, state_id=-1):
		'''SBList.order()
		Return a list of indexes that represent the 
		sorted order of the underlying list in this object.
		The order of the underlying list will not change.

		If start and end are specified, only that subset of indexes
		will be returned.

		THIS IS RETURNING INDEXES INTO self.l, AND NOT TO THE VIRTUAL LIST.
		I'M NOT SURE OF THAT IS WHAT I WANT TO DO.

		Optional keyword arguments for state_id, starting index,
		and ending index to order a subset of the virtual lines
		Use zero-based indexes with the ending index
		being a python slice() format index one greater than the last
		index-value to sort.
		'''
		if state_id == -1: state_id = self.state_id
		if end==0:
			end = self.get_llen(state_id=state_id) 
		if end==0:
			# Return an empty list if the logical length of the list is 0
			assert(6==7)
			return([])

		decorated = []
		for j in range(start, end):
			sd = self._get_l_idx(j, state_id=state_id)

			assert(sd.list_idx is not None)
			decorated.append([self.l[sd.list_idx], sd.list_idx])
		#
		decorated.sort()
		sorted_idx = []
		for t in decorated:
			sorted_idx.append(t[1])
		return(sorted_idx)

	def return_list(self, state_id=-1):
		'''SBList.return_list()
		Returns a list object that contains the view based
		on the specified state_id.

		MAYBE CHANGE THIS TO FOLLOW THE LOGIC OF __repr__,
		WHICH SHOULD BE FASTER.
		'''
		if len(self) == 0:
			assert(7==8)
			return([])

		new_l = []
		for j in range(len(self)):
			sd = self._get_l_idx(j)
			assert(sd.list_idx is not None)
			new_l.append(self.l[sd.list_idx])	
		return(new_l)

	def set_prior_state_id(self, i):
		'''Save the previous state ID so that it can be 
		accessed during operations that change states.
		'''
		self.prior_state_id = i
		return(0)

	def set_state_id(self, id):
		self.state_id = id
		return(0)

	def show_l(self):
		return( 'FOR DEBUGGING ONLY' + repr(self.l))

	def show_state(self, state_id=-1):
		'''SBList.show_state()
		This shows some debugging information about the 
		the indirection used to recreate the virtual rows
		from the main list.
		'''
		if state_id == -1: state_id = self.state_id
		return(repr(self.state[self.state_id]))
			
	def sort(self, state_id=-1, start=0, end=0):
		'''SBList.sort()
		Sort the virtual view of the underlying list object.
		This does not change the order of the underlying list
		but changes the virtual view of the items.
		Returns zero on success.
		
		Optional keyword arguments: state_id, start, and end,
		where start and end are zero-based python indexes and
		*end* is a pythonic ending index that is one greater than
		the index of the last item that you want to sort.
		'''
		#raise Exception("sort() is under construction. fix the subsort.")

		# This could be improved by finding a faster sort routine
		# or by merging the existing range into the first sort
		# range if applicable (and when start/end are not at the
		# extreme values).
		if state_id == -1: state_id = self.state_id
		if end==0:
			end = self.get_llen(state_id=state_id)

		# Get a sorted list of index values that point to self.l 
		# WAS THIS ORIGINALLY THE LENGTH OF END-START?
		sorted_indices = self.order(state_id=state_id, \
			start=start, end=end)

		self.incr_state_id()
		
		inside_is_done = False
		temp_l = self.get_state_with_vrows(state_id=state_id)
		#k = 0
		for storage_ref in temp_l:
			# 'storage_ref' contains [[l_start, l_end], [v_row_start, v_row_end]]
			#if storage_ref[1][1] <= start or storage_ref[1][0] > end:
			if storage_ref.logical_end <= start \
			or storage_ref.logical_start > end:
				# This range item in self.state is not in the sort range.
				# Keep this range as it is.
				self.state[self.state_id].append([storage_ref.storage_start, \
					storage_ref.storage_end])
			#	# This range item in self.state is a range that exactly
			#	# equals the target sort rows, so it doesn't need sorting.
			#	# Add it as it is
			#if storage_ref[0][0] < start and storage_ref[0][1] > start:
			if storage_ref.storage_start < start \
			and storage_ref.storage_end > start:
				# split the bottom part of the range before the sort
				self.state[self.state_id].append([storage_ref.storage_start, start])
			#
			# Now insert the sorted state indices:
			if not inside_is_done:
				len_indices = len(sorted_indices)	
				assert(len_indices == (end - start))
				i = 0
				while i < len_indices :
					j = i + 1
					# Identify contiguous storage_refs in the list of sorted
					# indices:
					while j < len_indices \
					and sorted_indices[j - 1] == (sorted_indices[j] - 1):
						j += 1
					self.state[self.state_id].append([sorted_indices[i], \
						sorted_indices[j - 1] + 1])
					i = j 
					inside_is_done = True

			#***********************************************
			# append any of the old ranges that overlapped the end
			# of the sort region and extended beyond it:
			#if storage_ref[1][0] < end and storage_ref[1][1] > end:
			if storage_ref.logical_start < end and storage_ref.logical_end > end:
				# The tail end of the old range overlaps the sort
				# range and extends beyond it. append the top part
				# of that range (the sort routin already grabbe the part
				# that was in the sort range).
				self.state[self.state_id].append([end, storage_ref.storage_end])
					
		return(0)


	def undo(self):
		'''SBList.undo()
		'''
		# Access the previous state id value from the log.
		# Remember that if the user used undo and then made edits, the
		# previous state value could point to nearly any of the valid
		# states.
		if self.state_id <= 1:
			self.state_id = 0
		else:
			self.state_id = self.log[self.state_id - 1][0]
		return(self.state_id)

	def update(self, v_row, val, state_id=-1, batch=False):
		'''SBList.update()
		Update the specified item with a new item.

		This is implemented by deleting the old item
		from the virtual representation of the underlying
		list and inserting the new version of that item 
		into the virtual representation of the underlying
		list.	The old item is not actually deleted, just
		not linked from the new state.
		'''
		if state_id == -1: state_id = self.state_id
		new_state_id = self.delete(v_row, state_id=state_id, batch=batch)
		new_state_id = self.insert(v_row, val, \
			state_id=new_state_id, batch=True)
		return(new_state_id)

def dprint(msg):
	pass
	#print(msg, file=sys.stderr)
