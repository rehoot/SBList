# THIS PROGRAM HAS MANY BUGS, BUT MIGHT BE USEFUL TO SOMEBODY.
# this will be a state-base list of strings
# The top class will contain all the insert and delete
# methods and will hold the state_id. 
# The log will contain list transactions and list/str
# transactions.

# ************* I CAN'T ALLOW THE USER TO INSERT DIRECTLY INTO THE SBSTRING OBJECT
# BECAUSE IT RUINS MY CAPTURE OF THE STATE_ID.  I NEED TO REDEFINE
# A BASE CLASS FOR SBSTRING THAT HAS A HIDDEN INSERT/DELETE METHOD
# THEN ALLOW CALLS ONLY FROM THE INITIATING OBJECT
#
# ADD 'STATEMENTS' OBJECT THAT TRACKS START/END PT
# FOR LOGICAL STATEMENTS (INCLUDING MULTI-LINE COMMANDS
# AND COMMENTS)
#
# ADD BOOKMARKS IN HERE, AND UPDATE FOR INSERT AND DELETE.
# Maybe use a special bookmark for multi-line formattin of 
# comment blocks (delete the mark when leading or trailing
# marker is delete?)
#
# 
import datetime
import os
import sys

from SBList import *
from SBString import *


class SBStrList(object):
	'''class SBStrList()
	This is a list of strings that is built
	on state-based objects that facilitate
	undo().
	'''
	class StorageRef(object):
		storage_start = None
		storage_end = None
		logical_start = None
		logical_end = None
		def __init__(self):#, storage_range, logical_range):
			object.__init__(self)
			
	class LogEntry():
			'''class SBStrList.LogEntry
			This holds information about one edit action.
			The properties are populated according to what makes
			sense for the given action.

			t_pt is a pointer into the text of the current line,
			not a global text pointer.
			sbstr will be an SBString object for line-deletion transaction 
			or line cut/paste.

			Action codes:
				'i' for insert text, 
				'd' for delete text,
				'il' = insertline, 
				'dl' = delete line. 
			Possible future codes would be 'm' for move-a-line, or 'u' for
			updated. Update is currently processed by a deletion and 
			an insert.
			'''
			action = None
			time = None
			old_lstate = None
			new_lstate = None
			old_str_state = None
			new_str_state = None
			row_idx = None
			t_pt = None
			txt = None
			sbstr = None
			def __init__(self, action, time, old_lstate, new_lstate, old_str_state, \
				new_str_state, row_idx, del_count=None, t_pt=None, txt=None, sbstr=None):
				'''UndoChanges.__init__
				'''
				self.action = action
				self.time = time
				self.old_lstate = old_lstate
				self.new_lstate = new_lstate
				self.old_str_state = old_str_state
				self.new_str_state = new_str_state
				self.row_idx = row_idx
				# for text edits only (not line insertion or deletion:
				self.t_pt = t_pt
				self.txt = txt
				# for line deletion, cut and paste
				self.sbstr # a SBString object
			def __repr__(self):
				'''log.__repr__
				'''
				return('[' + self.action + ', ' + self.time.strftime("%Y %h %d %H:%M:%S.") \
					+ str(self.time.time().microsecond) + ', ' \
					+ str(self.old_lstate) + ', ' + str(self.new_lstate) + ', ' \
					+ str(self.old_str_state) + ', ' + str(self.new_str_state) + ', ' \
					+ str(self.row_idx) + ', ' + repr(self.t_pt) + ', ' 
					+ repr(self.txt) + ']\n')
					

	def __init__(self, ListOfStrings):
		'''SBStrList.__init__()
		'''
		# MAYBE I SHOULD CODE ATTRIBUTES WITH THE VALUE OF THE
		# CURRENT INSTANCE SO EVERYTHING CAN GRAB THE CURRENT
		# STATE_ID WITHOUT REQUIRING INPUT FROM THE USER -- is that needed?
		object.__init__(self)
	
	
		# Cast the strings as SBSTring objects and load into a new list.
		# I tried embedding this into SBList, but it caused a loop in the 
		# definitions of SBList and SBString.
		self.buff_len = SBList([0])
		temp_l = []
		for j in range(len(ListOfStrings)):
			#if ListOfStrings[j][-1] not in ['\n', '\r'] \
			#and j != (len(ListOfStrings) - 1):
			#	temp_l.append(SBString(ListOfStrings[j]) + '\n')
			#else:
			if ListOfStrings[j][0:-1].count('\n') > 0:
				raise Exception('Your test string contains an embedded EOL in mid-line.')
			temp_l.append(SBString(ListOfStrings[j]))
			self.buff_len[0] += len(ListOfStrings[j])
		self.l = SBList(temp_l)
		#
		self.state_id = 0
		self.point = SBList([0])
		# The main state_id for SBStrList will be the state_id for
		# self.log?  To show the undo list of self.log, display
		# only values in the range self.log[0:self.log.get_state_id].
		# I might have to review how transactions
		# are chunked (such as 'replace' or 'update' transactions).
		self.log = SBList([]) 
		# Maybe use a list or function that lists all the 
		# objects that contain range-based lists so that users
		# can create one and have it automatically updated.
		self.range_lists = []
		self.range_funcs = []
		self.bookmarks = SBList([])
		# The *statements* field might be used to store the start and
		# end points of comment blocks or full statements in a
		# programming language. It might help the logic for applying
		# the syntax highligher by telling it to start on a prior line.
		self.statements = SBList([])
		self.range_lists.append(self.bookmarks)
		self.range_lists.append(self.statements)
		
		self.line_pts = None
		self.rebuild_line_pts()
		tmp_lp = None
		self.range_lists.append(self.line_pts)

	def __getitem__(self, x):
		# This returns an item from the main list based
		# on the virtual row index, *x*.	That index
		# can be a slice(), which is a range() specifed
		# in python format (i.e., the last index is one
		# greater than what you want returned).
		if x > len(self):
			raise IndexError
		if type(x) == type(slice(1,2)):
			temp = []
			if x.step is None:
				step = 1
			else:
				step = x.step
			for j in range(x.start, x.stop, step):
				temp.append(self.l[self.get_lrow_idx(j)])
			return(temp)
		else:
			# The requested item is not a slice:
			return(self.l[x])
			#return(self.l[self.get_lrow_idx(x)])

	def __iter__ (self): 
		# Maybe add a flag that will lock the objects from
		# being altered when iter is active?
		self.iterindex = len(self.l)
		return(self)

	def __len__(self):
		'''SBStrList.__len__()
		Returns the length of the virtual list object.
		'''
		return(len(self.l))

	
	def __next__ (self): 
		'''SBStrList.__next__()
		Return a list entry with each call.
		'''
		self.iterindex -= 1
		if self.iterindex < 0:
			raise StopIteration
		#
		# the countdown starts at the maximum value, but I want
		# to reverse the index to start at zero:
		new_idx = len(self.l) - self.iterindex - 1
		return(self.l[new_idx])

	def __repr__(self):
		#s = ''
		tmp_l = []
		for j in range(self.line_count()):
			#s += self.l[j].get_string()
			tmp_l.append(self.l[j].get_string())
		return(''.join(tmp_l))

	def __len__(self):
		return(len(self.l))

	def _dump(self, msg):
		'''SBStrList._dump()
		Dump many important objects to sys.stderr

		Run this program from the command line like this:
		env python sbed02.py -f infile.txt 2> debug.log
		where 2> is the redirection for stderr.
		'''
		dprint('---------------------------------------DUMP START')
		dprint(msg)
		dprint('')
		dprint('state_id= ' + str(self.state_id))
		dprint('point state id=' + str(self.point.get_state_id()) +' contents = ' + repr(self.point))
		dprint('log state id =' + str(self.log.get_state_id()) + ' contents=\n' + repr(self.log))
		dprint('line_pts state id= ' + str(self.line_pts.get_state_id()) + ', contents:\n' + repr(self.line_pts))
		dprint('self.l:\n' + repr(self.l))
		return(0)

	def add_bookmark(self, range):
		pass

	def add_statement(self, range):
		pass

	def add_range_list(self, lst):
		'''SBStrList.add_range_list(
		Add a list object that contains [start, end]
		pointers into the text using python slice()
		format.

		Lists entered here need corresponding entries
		loaded via add_range_updater() that are run
		via update_range_lists()
		'''
		self.rangelist.append(lst)
		return(0)
	
	def delete(self, pt, count, batch=False):
		# 1) Find the affected line
		# 2) determine if the full line is being deleted
		# 3) delete as needed
		# 4) update line_pts
		# 5) update bookmarks
		# 6) update statements
		idx = self.pt_to_line(pt)
		# Get the pointer within the appropriate text chunk:
		t_pt = self.pt_to_t_pt(pt)
		#
		save_lstate = self.l.get_state_id()
		save_str_state = self.l[idx].get_state_id()
		save_t_pt = t_pt	
		dprint('del a ' + str(self.l[idx].get_point()))
		self.l[idx].delete(t_pt,  count, batch=batch)
		dprint('del b ' + str(self.l[idx].get_point()))
		self.update_line_pts(pt, -1 * count, batch=batch)
		self.log.append(self.LogEntry('d', datetime.datetime.now(), save_lstate, \
			self.l.get_state_id(), save_str_state, \
			self.l[idx].get_state_id(), idx, t_pt=t_pt, del_count=count))
		return(0)

	def get_char(self, pt):
		idx = self.pt_to_line(pt)
		t_pt = self.pt_to_t_pt(pt)
		return(self.l[idx].get_char(t_pt))

	def get_lines(self, idx, count=1):
		pass

	def get_line_pts(self, idx):
		'''SBStrList.get_line_pts()
		return a range that contains the starting and ending
		points for the specified line in [star, end] slice()
		format.
		'''
		if idx > len(self.line_pts) or idx < 0:
			raise IndexError
		return(self.line_pts[idx])

	def get_point(self, state_id=-1):
		pass
	
	def get_str_list(self):
		'''StrList.get_str_list()
		Return a list object that contains the regular text
		stored in this object.
		'''
		tmp_l = []
		for j in range(len(self.l)):
			l.append(self.l[j].get_string())
		return(''.join(tmp_l))

	def goto_bookmark(self, bmark):
		# maybe use a dictionary to handle bookmarks,
		# so this arg would be the string name of the 
		# bookmark.
		pass	

	def insert(self, pt, txt, batch=False):
		# make all these methods so that they operate on
		# the current state (no state_id override)
		# Note: pt is the global point. t_point is the point
		# into the current text object.
		#
		# Function:
		# 1) Find the affected line
		# 2) determine if new lines are being created (embedded EOL)
		# 3) insert as needed
		# 4) update the log
		# 5) update line_pts
		# 6) update bookmarks
		# 7) update statements

		# TODO: consider keeping the EOL marker as the indicator of 
		# where existing SBString object will be copied.  In other
		# words, If I insert a block of text with embedded EOL,
		# the first part of the insertion would generate a new SBString
		# as if the existing EOL is fixed in concrete thereby forcing
		# the inserted lines to be inserted above.  This will help to
		# keep undo history predictable.  If an EOL marker is deleted,
		# then that SBString object will be deleted from the virtual view.
		idx = self.pt_to_line(pt)
		# Get the pointer within the appropriate text chunk:
		t_pt = self.pt_to_t_pt(pt)
		#
		save_lstate = self.l.get_state_id()
		save_str_state = self.l[idx].get_state_id()
		dprint('in SBStrList.insert a: str sid = ' + str(self.l[idx].get_state_id()) \
			+ ' lstateid = ' + str(self.l.get_state_id()) + ' batch is ' + repr(batch))
		save_t_pt = t_pt	
		# DO I NEED EXTRA LOGIC FOR NON-STANDARD EOL?
		lines = txt.split(os.linesep)
		end_txt = ''
		for j in range(len(lines)):
			if j == 0:
				# Insert the first part of the new text:
				self.l[idx].insert(t_pt, lines[j], batch=batch)
				dprint('in SBStrList.insert B: str sid = ' + str(self.l[idx].get_state_id()) \
					+ ' lstateid = ' + str(self.l.get_state_id()))
				self.update_line_pts(pt, len(lines[j]))
				pt += len(lines[j])
				if len(lines) > 1:
					# The insertion contains embedded EOL, so
					# delete the end of the line that was displaced by 
					# inserting the EOL (but leave the existing EOL)
					t_pt = self.pt_to_t_pt(pt)#pointer within this text chunck
					end_txt = self.l[idx].get_string()[t_pt:] 
					#print("multi-line insert, pt=" + str(pt) + ' deleting from tpt=' \
					#	+ str(t_pt) + ' endtxt= ' + end_txt)
					self.l[idx].delete(t_pt, len(end_txt), batch=True)
					self.update_line_pts(pt, -1 * len(end_txt))

					# Insert an EOL after the first insertion
					# (note that the last line in the file might not have had one)
					self.l[idx].insert(t_pt, '\n', batch=True)
					self.update_line_pts(pt, 1)
					pt += 1

					# Push the end of the insertion line to a new line.
					self.l.insert(idx + 1, SBString(end_txt ), batch=True)
					self.rebuild_line_pts()
					#self.update_line_pts(pt, len(end_txt) + 1)
					#pt += 1 #eol
			else:
				# Insert the second (or higher) line of new text.
				if len(lines[j]) != 0:
					if j == (len(lines) - 1):
						# The last portion of the split text in 'lines'
						# If it is empty, don't do anything, others insert 
						# the text into an existing SBText object
						t_pt = self.pt_to_t_pt(pt)#pointer within this text chunck
						self.l[idx + j].insert(t_pt, lines[j], batch=True)
						dprint('in SBStrList.insert B: str sid = ' + str(self.l[idx].get_state_id()) \
							+ ' lstateid = ' + str(self.l.get_state_id()))
						self.update_line_pts(pt, len(lines[j]))
						pt += len(lines[j])
					else:
						# This is a new, full line with EOL.
						# Insert a new line into the file.
						self.l.insert(idx + j, SBString(lines[j]), batch=True)
						# RUN REBUILD_LINE_PTS HERE !!!!!!!!!!!!!!!!!!!!!!!!
						self.update_line_pts(pt, len(lines[j]))
						pt += len(lines[j])
		# Now insert that end text at the end
		#if end_txt != '':
		#	t_pt = self.pt_to_t_pt(pt)#pointer within this text chunck
		#	print('Appending end, pt=' + str(pt) + ', tpt= ' + str(t_pt))
		#	print('chcking line nb ' + str(self.pt_to_line(pt)))
		#	self.l[idx].insert(t_pt, end_txt, batch=False)
		#	self.update_line_pts(pt, len(end_txt))
		#	print('line pts= ' + repr(self.line_pts))
		
			# Construct the log entry:	
		self.log.append(self.LogEntry('i', datetime.datetime.now(), save_lstate, \
			self.l.get_state_id(), save_str_state, \
			self.l[idx].get_state_id(), idx, t_pt=t_pt, txt=txt))
		self.buff_len[0] += len(txt)
		return(0)

	def insert_line(self, before_line, txt):
		pass

	def line_count(self):
		return(len(self.l))

	def list_bookmarks(self):
		pass

	def list_statements(self):
		pass

	def pt_to_line(self, pt):
		'''SBStrList.pt_to_line()
		Return the index number of the line that contains the
		specified point in the current state.
		'''
		#print(repr(self.line_pts))	
		found = False
		j = 0
		while not found and j < len(self.line_pts):
			if self.line_pts[j][0] <= pt and (self.line_pts[j][1] - 1) >= pt:
				found = True	
			j += 1
		return(j - 1)

	def pt_to_t_pt(self, pt):
		'''SBStrList.pt_to_t_pt()
		Convert a global point into the buffer to a t_pt,
		which is a zero-based index into the text at the current line
		'''
		line = self.pt_to_line(pt)
		assert( line >= 0)
		return(pt - self.line_pts[line][0])	

	def rebuild_line_pts(self):
		tmp_lp = []
		tmp_pt = 0
		for j in range(len(self.l)):
			# Record the starting and ending point on each line.
			# This is NOT in slice() format.
			tmp_lp.append([tmp_pt, tmp_pt + len(self.l[j])])
			tmp_pt += len(self.l[j])
		self.line_pts = SBList(tmp_lp)
		return(0)

	def redo(self):
		pass

	def set_bookmark(self, pt_start, len):
		pass

	def show_line_pts(self):
		'''SBStrList.show_line_pts()
		This is for debugging purposes to show the saved
		list of starting and ending points (slice() format)
		for each buffer line.
		'''
		return(repr(self.line_pts))

	def show_undo_list(self):
		return(repr(self.log))

	def set_point(self, pt):
		pass

	def str_len(self):
		'''SbStrList.str_len()
		Return the full length of the buffer in characters.
		'''
		#ln = 0
		#for sbs in self.l:
		#	ln += len(sbs)
		#return(ln)
		reuturn(self.buff_len[0])

	def list_len(self):
		return(len(self.l))

	def undo(self):
		if len(self.log) == 0:
			return(0)

		top_state_id = self.log.get_state_id()
		#top_log_entry = self.log[-1]
		#self.log[0:self.log.get_state_id]
		top_log_entry = self.log[top_state_id]
		top_action_code = top_log_entry.action
		top_idx = top_log_entry.row_idx
		# The undo() below undoes the record of the transaction
		# and thereby leaves the top entry with the l_state and
		# v_state IDs that are desired.
		# ONE UNDO ON THE LOG ENTRY WILL NOT UNDO MANY BATCH ENTRIES !!!!!!!!!!!!!!!!!!!!i!!!!!!!
		self.log.undo() #this undoes only the transaction
		if top_action_code in ['i', 'd']:
			#print('UNDO TEXT EDIT for line idx ' + str(top_idx))
			self.l[top_idx].undo(count=1)
			self.buff_len.undo()
		else:
			raise Exception ("not ready to undo line-oriented actions")
		
		pass

	def update_line_pts(self, pt, incr, batch=False):
		'''SBStrList.update_line_pts()
		Update self.line_pts to reflect inserted or deleted
		text. Do NOT call this if there are new or delete lines.
	  self.line_pts is a list of the starting points
		and ending points for each line.

		see also: rebuild_line_pts
		'''
		idx = self.pt_to_line(pt)
		# I will delete all the existing range entries and then append
		# new ones
		old_lp_state = self.line_pts.get_state_id()
		b_code = batch
		len_pts = len(self.line_pts) 
		save_line_pts = []
		for j in range(len_pts):
			# Save the current state of line_pts because if actions
			# are taken in batch mode, I'll need this to get the 
			# prior state.
			save_line_pts.append(self.line_pts[j])

		for j in range(len_pts -1, idx - 1 , -1):
			self.line_pts.delete(j, batch=b_code)
			b_code = True

		# Now insert the updated entries (there might be new or delete rows)
		for j in range(idx, len(save_line_pts)):
			# The current state of self.line_pts should contain one entry 
			# for each record in self.l. Get that entry to find the starting and
			# ending point for each line:
			low = save_line_pts[j][0]
			high = save_line_pts[j][1]
			if low <= pt:
				self.line_pts.append([low , high+ incr], batch=True)
			else:
				self.line_pts.append([low + incr, high+ incr], batch=True)

		return(0)

	def update_range_lists(self, pt, incr):
		'''SBStrList.update_ranges()
		Update all the list objects that contain ranges of 
		start/end points.  This processes anything that was
		registered with add_range_list()

		see also: rebuild_line_pts
		'''
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		# MODIFY THIS TO MAKE IT GENERIC FOR THE REGISTERED LISTSV
		idx = self.pt_to_line(pt)
		# I will delete all the existing range entries and then append
		# new ones
		old_lp_state = self.line_pts.get_state_id()
		b_code = False
		for j in range(idx, len(self.line_pts)):
			self.line_pts.delete(idx, batch=b_code)
			b_code = True

		# Now insert the updated entries (there might be new or delete rows)
		for j in range(idx, len(self.l)):
			low = self.line_pts.get_item(j, state_id=old_lp_state)[0]
			high = self.line_pts.get_item(j, state_id=old_lp_state)[1]
			if low < pt:
				self.line_pts.append([low , high+ incr], batch=True)
			else:
				self.line_pts.append([low + incr, high+ incr], batch=True)

		return(0)

def dprint(str):
	#pass
	print(str, file=sys.stderr)

