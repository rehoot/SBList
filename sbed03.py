# sbed03.py = an editor built on my state-based list and string objects
# cat bobed01.py |grep '^class\|^[       ]*def '|less
# Note, non BSD-ish UNIX might not be able to run this as a script
#
# cat sbed02.py |grep  -E -e "[^[:graph:]]*def" -e ^class|less
# If the screen is ruined after this program exits, run my
# fixscreen.sh script, which uses stty commands to reset
# the screen attributes, and you must run it with the ". "
# prefix: ". fixscreen.sh"
#
# Unicode problem in python curses: http://bugs.python.org/issue6745
# Another post says that the real ncurses uses get_wch to input
# unicode http://tinyurl.com/3wudz37, but maybe I can manually input
# extra chars?
'''

#Compile by running:
import py_compile
py_compile.compile('sbed02.py')
import sbed02
help(sbed02)

Debugger Menu command: Tools/Debugger
debugger location
/opt/local/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/pdb.py
'''
#
#TO DO:
# 
# * A SHELL SCRIPT THAT LOADS AND RUNS THE COMPIELD .pyc.
#   THAT APPROACH COULD MEAN FASTER LOADING
# * write the line-break program and feed the results
#   to sbstrlist.line_rage or whatever I called it.
# * BUILD A TRACING ROUTINE THAT DUMPS IMPORTANT INFORMATION
#   TO A TRACING DIRECTORY SPECIFIED IN THE -t OPTION.
#
##############################################################
# temp notes:
##############################################################
# 
#
#
# OLD STUFF
# Use list objects for each input record:
#   record object: 
#      rec_type, 
#      string, 
#      line-format object,
#      display visibility (start/stop or by character)
#      highlighting object (multiple objects),
#      calculted: text as displayed
#      line comment
#      reference to external file
#      sticky notes attached to a line
#      meta (create date, user ID,...))
#
#   line-format object:
#      starting offset, attr
#   highlighting object:
#      same as line-format, but used to highlight
#      text for note-taking and will be toggled
#      independently of syntax highlighting.
# The LRECL of the string in the list = the display width.
# the start of a real line is type 1, a continuation
# is type 2.  Try to break on spaces, leaving the space
# at the end of the previous line.
#
# TABS: I need to resolve the display of tab characters
# versus where they are in the buffer -- the window
# offset differs from the buffer offset
# Maybe put nulls into the buffer to fill for tabs
# then remove them before saving!
#
# text marker for hidden text: 'x\u20e3' (combining rouned box)
# or \u20dd
#
#####################################################################
# FUTURE FEATURES (pie in the sky version):
# * maybe create flags for internal use: local point_start_update_needed,
#   global_point_start_update_needed
# 0.1.0 a structured way to run regular python against
#       ibuff (or a copy of it) then reload the editor
#       when done (no need to use the text editory 
#       functions).
# 0.1.0.5 view debug comments on the left in their own
#       window as glued to the input lines on the left
#	      window. Expand the comment into a window if the
#	      comments have many lines. these would be different
#       from 'section comment' that might collapse into 
#       one line but really refer to a range if code lines.
# 0.1.1 find/replace with highlighting
# 0.1.2 display a status bar at the bottom with both
#    visual and input buffer row/col, pct of file
# 0.1.3 system clipboard cut and paste
# 0.1.3.1 kill ring, but rename it
# 0.1.4 customizable file/open dialog so that the 
# 0.1.5 optional hard LRECL with optional space padding
#    and optional hard-coded line numbers (with some
#		 enforcement of formatting). maybe put the line numbers
#	   in the line number window and the write them to the file.
# 0.1.6 SPF stile line markers
#    default search filter can be set in the options
#    file and the user can define other custom sets
#    or type one in the search box.
# 0.2 vertical split window with the windows row-locked
#	0.3 encrypted swap file and encrypted files (with
#    all files using the same password)
# 1. undo using difflib.pyc.  when a user edits a line
#    the line is saved and a diff is created when the
#    user leaves the line.  A 'u' is displayed in the 
#    left margin to indicate undo information.  When
#    the user presses teh right key, a list of undo
#    history is displayed.  insertion EOL will keep the
#    undo information on the first line. deleted lines
#    will be stored in the line above the deletion area.
# 1.1 scripting from a pop-up window. I might be able to
#    use the ast module to evaluate:
#    ast.literal_eval('s = 'ab' + len(q)')
#    for python 2.6 and higher
# 1.2 report viewing:
#    a) lock headers and columns for scrolling
#    b) when the cursor is on a number, a side window
#    c) shows dictionary pairs, like the number for a keyboard
#       value shown in a trace listing is decoded to a letter.
#       maybe it reads the header row and does context-
#       sensitive decoding based on header.
#    d) highlight row and column like SPF
#    e) automatic greenbar highlighting based on file row num
#    f) tab to move between data fields
#    g) works in org mode too
# 2. highlighting. creates one set of regexp lists for
#    syntax highlighting, another for spelling highlighting,
#    one for search, one for user. define a hierarchy
#    for them.
# 3. collapsing comments: one comment symbol leaves the
#    comment as usual.  two symbols collapses the comment
#    and glues it to the next real line.  hidden comments
#    will be associated with a symbol in the left column
#    and can be displayed if the user presses the right key.
#    three comment symbols means collaps it and leave it 
#    in a row that displays a dashed, grayed line.
# 3.1 Allow export of the file with the specified level of
#    comments promoted to regular text, but keep the current
#    file with comments as is.
# 4. dynamic list of class or function completions.  maybe
#    display the completions in a window on the right side.
# 5. background spelling (separate thread?)
# 6. tabbed browsing
# 7. modified display format for XML along with XML templates
#    to help organize and structure notes or documents?
# 8. hex mode
# 9. create a full copy of the input file that has been
#    cleaned of all comments. use this as the basis for
#    spelling, function goto-menu, syntax checker, etx.
#    Maybe segment the vchunks to allow for a quick
#    virtual list. Allow for an array of flags for
#    vchunks, with the main list containing flags
#    for leading whitespace, code, trailing whitespace,
#    and comment (where space after code and before
#    comment is still trailing whitespace).
# 10. option for sticky point on each line (as you move
#    up/down, the point on that line is the last place
#    according to the last left/right movement.
#    Or maybe flash the charcter where the point had been
#    or put a tiny frame in the previous edit region
#    but leave cursor motion as normal.
# 10.5 add an option to highlight all edits since the original.
#    do this by highlighting when the storage location is
#    beyond the original EOF.
# 11. bookmarks and lines with extended notes.  Warn of a deletion will
#    delete a note--the option will be to stick the note to the 
#    next character. Note storage: put notes at the end of the file
#    after a header and with entries like:
#    #NOTE32 CRC12345 PERFORMANCE 2011102723:32 -7 text of note
#    NOTE32 = line 32, CRC123 woul be the CRC32 value for that line
#    followed by a category name and GMC time with offset.
#    categories: performance, change, general, testing, translation,
#    template, wizard, syntax checker, review, approval
#    and 'writer categories:' plot, character, timeline, setting,
#    motivation, evidence, grammar, spelling and usage, pace.
# 11.1 store permanent bookmarks at the bottom of the file similar
#    to notes:
#    #BM32 100 123 CRC# Name 2011102723:32 -7 text of note
#    where 100 and 123 are point start and end, and CRC is the
#    crc for that chunk
# 11.5 bookmarks to mark outline items. The driver function takes
#    a statement (usually 1 or 2 buffer input lines) and returns
#    true or false.  This would require the STATEMENT parser.
#    also allow for keyword spec to build an alternative outline.
# 12 knuth-style self-documenting code that sends level-1 comments
#    to latex after appropriate formatting by a 'print' command.
#    The editor will apply appropriate commands around code to
#    print it using lstlisting, use special bookmarks to flag
#    the license agreement so it can be printed in the documentation,
#    maybe a hidden note that contains the latex head and preamble,
#    built-in latex checker,
#	13 provide an 'x all' command to hide all lines that contain
#    the specified regexp
# 14 Integrated bibtex to resolve citations and referenes without
#    latex
# 15 python templates with a checklist for options like:
#    curses, tkinter, qt4, getopt, file input, file output,
#    followed by a popup message about where to start and some
#    embedded notes with tips
#####################################################################

from SBStrList import *
import codecs
import configparser
import curses
import getopt
import os
import locale # for curses unicode setup
import re
import sys
import time
import traceback
import unicodedata

MAX_LRECL = 100
g_debug_level = 0
g_my_codec = 'UTF8'
g_trace_dir = './'
STATUSLINE_IDX = 0
MENU_LINES = 6
# YFUDGE: curses doesn't let me print in the bottom-right cell
# in (2010 on Mac) so the main display area will be shrunk by one row. I 
# couldn't set the filter() option, which might have helped.
YFUDGE = 1
# constants and settings:
TABWIDTH = 2# I'll need to detect tabwidth?
LINENUM = True
LINENUM_COL = 0 # window offset for displaying optical rowum
LINENUM_WIDTH = 6
TOPROW = 0 # clarify the meaning of zero
WHITE_SPACE = [' ', '\t']
TRACE_FNAME =  'pm.log'

class MainWindow():
	''' a global window class
	The parm for window should be the entire screen.
	This will then make a subwindow for the text display
	'''
	def __init__(self, window, buff):
		global 	STATUSLINE_IDX, g_trace_dir, g_my_codec
		#
		#self.txt = SBStrList(['Edit this string\n', 'This is line2\n'])# single line of text
		self.txt = SBStrList(buff)
		oldmouse = curses.mousemask(curses.BUTTON1_CLICKED)
		(max_y, max_x) = window.getmaxyx()
		self.framewin = window.subwin(max_y - MENU_LINES - 1 , max_x, MENU_LINES + 1, 0)
		self.scrn = window.subwin(max_y - MENU_LINES - 3, max_x - 2, MENU_LINES + 2, 1)
		self.line_ptr = 0 # THIS SHOULD BE IN txt.l
		self.scrn.keypad(1)
		curses.flushinp()	
		self.framewin.border()
		self.framewin.refresh()
		self.scrn.refresh()
		# pointasdf has a crazy name so that end-users don't
		# access it by mistake.  Users should use the porcelain
		# commands.
		self.pointasdf = 0 # This is the main point. Don't change this directly
		# the main point is now in self.txt.get_point and set_point
		self.width = self.scrn.getmaxyx()[1]
		self.height = self.scrn.getmaxyx()[0] - YFUDGE
		STATUSLINE_IDX = self.height - 1 + YFUDGE
		self.menuscrn = window.derwin(MENU_LINES, max_x, 0, 0)
		self.menuscrn.addstr(0,0, 'This program can be used to test the '
			+ 'SBString object. It is a one-line text editor.')
		self.menuscrn.refresh()
		#
		self.statusscrn = window.subwin(1, max_x, max_y - 1, 0)
		# setup required for curses to use unicode
		locale.setlocale(locale.LC_ALL, '')
		# use 'code' with str.encode() for curses display?
		g_my_codec = locale.getpreferredencoding()
		#
		# Initialize the display buffer that will hold
		# text according to lrecl
		# cursor location, based on physical window, not logical window
		self.winrow_idx = 0 #self.winmintxtrow_idx
		self.wincol_idx =  0 #self.winmintxtcol_idx
		#
		#self.displayscreen(self.startbuffrow_idx)
		#w_vp = self.get_wintxt_vp()
		(max_y, max_x) = self.scrn.getmaxyx()
		max_y -= YFUDGE
		self.scrn.clear()
		self.winrow_idx = 0
		self.wincol_idx = 0
		self.scrn.move(TOPROW , self.wincol_idx)
		self.display_line()
		##self.vbuff.display_screen(0, self.scrn)
		if g_trace_dir != '':
			self.trace_init()
		#self.unicode_test()

	def key_loop(self):
		'''MainWindow.key_loop
		After the calling routine instantiates this class
		it should call this function to capture input from the
		user and edit the input buffer.
		'''
		global g_my_codec

		savedigit = '' # numeric prefix for vim commands
		i = 0
		while True:
			self.trace('key ' + chr(i), key_nbr=i)
			i = self.scrn.getch()
			if 0<i<256:
				c = chr(i)
				if i == 127:
					# deletekey
					self.delete(-1)
				elif i == 27:
					# ESC key
					pass
				######else:				
				elif c == 'k':
					if savedigit == '':
						pass
						self.updown(-1)
					else:
						pass
						self.updown(int(savedigit) * -1)
						savedigit = ''
				elif c == 'j':
					if savedigit == '':
						self.updown (1)
						pass
					else:
						self.updown(int(savedigit))
						pass
						savedigit = ''
				elif c == 'J':
					if savedigit == '':
						pass
						#self.join(self.ibuff.bidx.get_row_idx())
					else:
						pass
						#self.join(int(savedigit))
						savedigit = ''
				elif c == 'h':
					if savedigit == '':
						self.leftright (-1)
					else:
						self.leftright(int(savedigit) * -1)
						savedigit = ''
				elif c == 'l':
					if savedigit == '':
						self.leftright (1)
					else:
						self.leftright(int(savedigit))
						savedigit = ''
				elif c == 'i':
					savedigit = ''
					self.insert_txt('i')
				elif c == 'a':
					savedigit = ''
					self.insert_txt('a')
				elif c == '$':
					savedigit = ''
					self.end_of_line()
				elif c == '0':
					if savedigit == '':
						self.beginning_of_line()
					else:
						# if somebody already started entering a numeric
						# prefix, keep accumulating it:
						savedigit += '0'
				elif c == 'w':
					if savedigit == '':
						self.word_forward('s', 1)
					else:
						self.word_forward('s', int(savedigit))
						savedigit = ''
				elif c == 'b':
					if savedigit == '':
						self.word_forward('s', -1)
					else:
						self.word_forward('s', int(savedigit) * -1)
						savedigit = ''
				elif c == 'e':
					if savedigit == '':
						self.word_forward('e', 1)
					else:
						self.word_forward('e', int(savedigit))
						savedigit = ''
				elif c == 'E':
					if savedigit == '':
						self.word_forward('e', -1)
					else:
						self.word_forward('e', int(savedigit) * -1)
						savedigit = ''
				elif c == 't':
					# move this logic into the window class
					# and higlight the current line
					savedigit = ''
					#self.top_of_screen()
				elif c == '?':
					pass
				elif c == 'b':
					# move this into the window class
					savedigit = ''
					#self.bottom_of_screen()
				elif c == 'k':
					savedigit = ''
					#self.kill()
				elif c == 'u':
					self.undo()
				elif c == 'x':
					if savedigit == '':
						# deletekey
						self.delete(1)
					else:
						self.delete(int(savedigit))
						savedigit = ''
				elif c == 'q':
					# Exit (quit) the program
					break
				elif c == ':':
					(saverow, savecol) = self.scrn.getyx()
					#self.statusscrn.leaveok(1)
					self.statusscrn.addstr(0, 0, ':', curses.color_pair(3))
					self.statusscrn.refresh()
					#self.menuscrn.leaveok(0)
					self.scrn.refresh()# set focus to main window
					##self.scrn.move(TOPROW, self.txt[self.line_ptr].get_point())	
					swincol = 0
					i = 0 
					cmd = ''
					while chr(i) not in ['\n', '\r']:
						# Collect the text of the : command:
						#
						i = self.statusscrn.getch()
						c = chr(i)
						if c not in ['\n', '\r']:
							# Display the entered character on the screen:
							self.statusscrn.addstr(0, swincol, c, curses.color_pair(3))
						# Adjust the cursor position
						swincol += 1
						# process backspace...!!!!! ADD CODE HERE!!!!!
						#
						# Accumulate the full command to be used later
						cmd += chr(i)
					if cmd[0] == 'w':
						# This is the 'write' command, look for the destination file name.
						swincol = 2
						# The command needs to separate the 'w' from the filename,
						# so this grabs the filename after the space:
						file = os.path.normpath(os.path.expanduser(cmd.split()[1]))
						if os.access(file, os.F_OK):
							# file exists
							prompt = 'Do you want to OVERWRITE: ' + file + '?'
						else:
							prompt = 'Do you want to write to: ' + file + '?'
						yn = ''
						self.file_save(file)
						#self.statusscrn.addstr(0, 1, prompt, curses.color_pair(3)) 
						#while yn.upper() not in ['Y', 'N']:
						#	yn = chr(self.scrn.getch())
						#if yn.upper() == 'Y':
						#	fdo = codecs.open(file, 'w', g_my_codec)
						#	for s in self.ibuff:
						#		fdo.write(s)
						#	fdo.close()
					else:
						pass
						# Dump other commands for now
					# Clear the satus area. Note that I avoid writing to the 
					# last cell in the bottom-right corner due to a problem
					# setting the 'filter()' function to deal with EOL
					# and because of a random error writing there.
					self.scrn.addstr(STATUSLINE_IDX, 0, ' ' * (self.width - 2))
					#
					self.scrn.leaveok(0)
					self.wincol_idx = savecol
					self.winrow_idx = saverow
					self.scrn.move(saverow, savecol)
					#self.scrn.move(TOPROW, self.txt[self.line_ptr].get_point())	
				elif c.isdigit():
					# the vim code of zero to move to the start of the line
					# can ruin this, so i'll fix the BOL code
					savedigit += c
				else:
					savedigit = ''
			else:
				# control keys or special characters?
				if i == curses.KEY_LEFT:
					if savedigit == '':
						self.leftright (-1)
					else:
						self.leftright(int(savedigit) * -1)
						savedigit = ''
				elif i == curses.KEY_RIGHT:
					if savedigit == '':
						self.leftright (1)
					else:
						self.leftright(int(savedigit))
						savedigit = ''
				elif i == curses.KEY_UP:
					if savedigit == '':
						self.updown(-1)
					else:
						self.updown(int(savedigit) * -1)
						savedigit = ''
				elif i == curses.KEY_DOWN:
					if savedigit == '':
						self.updown (1)
					else:
						self.updown(int(savedigit))
						savedigit = ''
				elif i == curses.KEY_NPAGE:
					# NEXT PAGE/ PAGE DOWN
					self.updown(self.height)
				elif i == curses.KEY_PPAGE:
					# PRIOR PAGE/ PAGE UP
					self.updown(-1 * self.height)
		return(0)

	def delete(self, incr):
		'''Delete characters.
		A negative number means delete to the left.
		A positive number means delete to the right
		'''
		# consider these curses functions clrtoeol (delete to eol)
		# clrtobot (clear to bottom of window)
		# delch (delete char at y,x)
		# deleteln() 
		if incr < 0:
			direction = -1
			adj = -1
		else:
			direction = 1
			adj = 0
		dprint('del a ' + str(self.txt[self.line_ptr].get_point()))
		# how many chars remain after the deletion is made:
		remaining_chars = len(self.txt[self.line_ptr]) - self.txt[self.line_ptr].get_point()
		if remaining_chars < 0:
			curses.beep()
			incr += remaining_chars 
			self.txt[self.line_ptr].delete(self.txt[self.line_ptr].get_point() \
				+ incr, incr)# self.txt[self.line_ptr].get_point())
		else:
			self.txt[self.line_ptr].delete(self.txt[self.line_ptr].get_point(), \
				incr)#self.txt[self.line_ptr].get_point() + incr)
		dprint('del b ' + str(self.txt[self.line_ptr].get_point()))
		# self.pointasdf does not change for delete.
		#
		#self.display_line()
		for j in range(incr * direction):
			self.win_del_char(self.scrn, self.line_ptr, self.txt[self.line_ptr].get_point() + adj)
			if direction < 0:
				adj -= 1
		return(0)

	def beginning_of_line(self):
		save_pt = self.txt[self.line_ptr].get_point()
		self.txt[self.line_ptr].set_point(0)
		self.display_line()
		self.pointasdf += self.txt[self.line_ptr].get_point() - save_pt
		return(0)

	def end_of_line(self):
		save_pt = self.txt[self.line_ptr].get_point()
		self.txt[self.line_ptr].set_point(len(self.txt[self.line_ptr]) - 1)
		if self.txt[self.line_ptr].get_point() > self.width:
			self.txt[self.line_ptr].set_point(self.width - 1)
		self.pointasdf += self.txt[self.line_ptr].get_point() - save_pt
		self.display_line()
		return(0)

	def insert_txt(self, mode):
		'''MainWindow.insert_txt()

		Insert text at the current cursor location.
		If mode = 'i', then insert text starting at the 
		cursor location.
		If mode = 'a' then insert after the current character.
		'''
		global g_my_codec

		(max_y, max_x) = self.scrn.getmaxyx()
		max_y -= YFUDGE
		vline_len = len(self.txt[self.line_ptr])
		if mode == 'a':
			# 'a' means insert text after the current character,
			# so increment the column if there is room to do so.
				self.incr_point(1)# Also adjusts cursor
		i = self.scrn.getch()
		b_mode = False
		#while i not in [27, 10, 13] and self.wincol_idx < max_x :
		while i not in [27] and self.wincol_idx < (max_x - 1) :
			# while ESC not pressed	
			#if i > 126 or i < 20:
			#	c = chr(i).encode(g_my_codec)
			#else:
			c = chr(i)
			self.status_message(ch=c)#show for debugging
			if i > 127:
				curses.beep()
				if i >> 6 == 3:
					# This is a two-byte unicode character
					i2 = self.scrn.getch()
					b = bytes([i, i2])
					c = b.decode(g_my_codec)
				if i >> 6 == 7:
					# three byte unicode character
					i2 = self.scrn.getch()
					i3 = self.scrn.getch()
					b = bytes([i, i2, i3])
					c = b.decode(g_my_codec)
					 	
			if (len(self.txt[self.line_ptr]) < (max_x - 1) \
			and len(self.txt) < (max_x - 1) and i >= 32) \
			or c == os.linesep:
				# Exclude control characters below 0x20 = 32decimal
				#self.txt[self.line_ptr].insert(self.txt[self.line_ptr].get_point(), c)	
				self.txt.insert(self.pointasdf, c, batch=b_mode)
				b_mode = True
				self.incr_point(1)# also adjusts cursor
				#self.display_line()
				self.win_ins_char(self.scrn, self.line_ptr, self.txt[self.line_ptr].get_point() - 1, c)
			else:
				# FOR THIS CRIPPLED VERSION, DON'T PROCESS EXTRA CHARACTERS
				self.menuscrn.leaveok(1) #set flag to leave cursor alone
				self.menuscrn.addstr(MENU_LINES - 1, 0, 'ERROR. LINES MUST FIT ON THE SCREEN.')
				self.menuscrn.refresh()
				self.menuscrn.leaveok(0)
			i = self.scrn.getch()
		return(0)

	def display_line(self):
		# Assume single-screen display in which each line is less than the
		# screen width
		#
		##self.scrn.addstr(0, 0, 'pt is ' + str(self.txt[self.line_ptr].get_point()))
		##junkjunkjunk = self.scrn.getch()
		list_len = len(self.txt)
		(max_y, max_x) = self.scrn.getmaxyx()
		for j in range(list_len):
			assert(j < (max_y - YFUDGE))
			# display blanks to clear prior line # IS THERE A CLEAR-WINDOW() COMMAND?
			self.scrn.hline(j, 0, '-', self.width)
			self.scrn.addstr(j, 0, self.txt[j].get_string(), curses.A_NORMAL)
		#
		self.update_status()
		#self.framewin.border()
		self.scrn.move(self.line_ptr,  self.txt[self.line_ptr].get_point())
		self.scrn.refresh()
		return(0)

	def file_save(self, fname):
		'''sbed02.file_save()
		Save the current buffer.
		'''
		global g_my_codec
		
		fname_clean = os.path.realpath(os.path.expanduser(fname))
		fbase_dir = os.path.dirname(fname_clean)
		if not os.access(fbase_dir, os.W_OK):
			# Display error message for the user:
			#raise Exception('Write access to output directory denied: ' \
			self.status_message(msg='ERROR, CANNOT WRITE TO OUTPUT FILE: ' + str(fname_clean))
			return(-1)
		fdo = codecs.open(fname_clean, 'w', g_my_codec)
		for sb in self.txt:
			fdo.write(sb.get_string())
		fdo.close
		return(0)

	def word_forward(self, mode, incr):
		'''word_forward()
		the mode flag is 'e' to move to the end of
		words or 's' to move to the start of words
		'''
		save_pt = self.txt[self.line_ptr].get_point()
		if incr < 0:
			direction = -1
		else:
			direction = 1

		mytxt = self.txt[self.line_ptr].get_string()
		
		j = self.txt[self.line_ptr].get_point()
		max = len(self.txt[self.line_ptr])
	
		for wcount in range(abs(incr)):	
			if j < max and j >= 0 and mytxt[j] in [' ', '\t']:
				# I am starting on a space, so skip forward
				# to the start of the next word
				while j < max and j >= 0 and mytxt[j]  in [' ', '\t']:
					j += direction
				if direction < 0 and mode == 's':
					while j < max and j >= 0 and mytxt[j]  not in [' ', '\t']:
						j += direction
					j += 1
				break
					
			# I am not starting on a space
			if direction < 0:
				# Peak backward to see if the previous char is a space
				if j > 0 and mytxt[j - 1] in [' ', '\t']:
					j -= 1
					while j < max and j >= 0 and mytxt[j]  in [' ', '\t']:
						j += direction
					
			else:
				if mode == 'e':
					# Peak forward to see if the previous char is a space
					if j < (max - 1) and mytxt[j + 1] in [' ', '\t']:
						j += 1
						while j < max and j >= 0 and mytxt[j]  in [' ', '\t']:
							# move to the start of the next word so 'e' moves
							# can continue below
							j += direction

			# Move until I find whitespace
			while j < max and j >= 0 and mytxt[j] not in [' ', '\t']:
				j += direction
			if direction > 0:
				if mode  == 's':
					# now go past the whitespace to find the start of 
					# nonwhitespace
					while j < max and j >= 0 and mytxt[j]  in [' ', '\t']:
						j += direction
				else:
					j -= 1
			else:
				if mode == 's':
					j += 1
				else:
					# Bacward 'e' move:
					while j < max and j >= 0 and mytxt[j]  in [' ', '\t']:
						j += direction
			
		self.txt[self.line_ptr].set_point(j)
		self.pointasdf += j - save_pt
		self.display_line()
		return(0)

	def leftright(self, incr):
		save_pt = self.txt[self.line_ptr].get_point()
		self.txt[self.line_ptr].incr_point(incr)
		if self.txt[self.line_ptr].get_point() >= self.width:
			self.txt[self.line_ptr].set_point(self.width - 1)
		self.pointasdf += self.txt[self.line_ptr].get_point() - save_pt
		self.scrn.move(self.line_ptr, self.txt[self.line_ptr].get_point())
		self.update_status()
		#self.display_line()
		return(0)
	
	def incr_point(self, incr):
		save_point = self.pointasdf
		save_line_ptr = self.line_ptr
		#
		self.pointasdf += incr
		if self.pointasdf < 0:
			self.pointasdf = 0
		# ADD THE TEST FOR MAX BUFFER LEN
		#if self.pointasdf >= self.txt.buffer_len():
		buffer_len  = self.txt.get_line_pts(len(self.txt) - 1)[1]
		if self.pointasdf >= buffer_len:
			self.pointasdf = buffer_len - 1

		self.line_ptr = self.txt.pt_to_line(self.pointasdf)
		if self.line_ptr > save_line_ptr:
			t_incr = self.pointasdf - self.txt.get_line_pts(self.line_ptr)[0]
			self.txt[self.line_ptr].set_point(t_incr)
		elif self.line_ptr < save_line_ptr:
			t_incr = self.pointasdf - self.txt.get_line_pts(self.line_ptr)[1]
			line_len = len(self.txt[self.line_ptr])
			self.txt[self.line_ptr].set_point(line_len + t_incr)
		else:
			self.txt[self.line_ptr].incr_point(incr)
		self.wincol_idx = self.txt[self.line_ptr].get_point()	
		self.scrn.move(self.line_ptr, self.txt[self.line_ptr].get_point())	
		#raise Exception('For testing, line width cannot exceed screen width')
		return(0)

	def undo(self):
		save_t_pt = self.txt[self.line_ptr].get_point()
		self.txt[self.line_ptr].undo(1)
		self.pointasdf = self.pointasdf - save_t_pt + self.txt[self.line_ptr].get_point()
		self.display_line()
		#i = self.scrn.getch()
		#self.scrn.move(self.line_ptr, self.txt[self.line_ptr].get_point())
		#self.scrn.refresh()
		return(0)

	def updown(self, count):
		(max_y, max_x) = self.scrn.getmaxyx()
		self.line_ptr += count
		if self.line_ptr < 0:
			self.line_ptr = 0
		if self.line_ptr >= (max_y - YFUDGE):
			self.line_ptr = max_y - YFUDGE - 1
		if self.line_ptr >= len(self.txt):
			self.line_ptr = len(self.txt) - 1
		self.pointasdf = 0
		for j in range(self.line_ptr):
			self.pointasdf += len(self.txt[j])
		self.pointasdf += self.txt[self.line_ptr].get_point()
		self.update_status()
		self.scrn.move(self.line_ptr, self.txt[self.line_ptr].get_point())
		self.scrn.refresh()
		return(0)
	
	def status_message(self, ch='', msg=''):
		global g_my_codec

		(save_y, save_x) = self.scrn.getyx()
		self.menuscrn.leaveok(1) #set flag to leave cursor alone
		if ch != '':
			self.menuscrn.addstr(1, 50, str(ord(ch)) + '   ')
		elif msg != '':
			self.menuscrn.addstr(3, 0, msg)

		self.menuscrn.refresh()
		self.menuscrn.leaveok(0)
		self.scrn.move(save_y, save_x)
		return(0)
	
	def update_status(self):
		global g_my_codec

		(save_y, save_x) = self.scrn.getyx()
		self.menuscrn.leaveok(1) #set flag to leave cursor alone
		self.menuscrn.addstr(1, 0, \
			  'sbpt:' + str(self.txt[self.line_ptr].get_point()) \
			+ ', ptasdf ' + str(self.pointasdf) \
			+ ', line: ' + str(self.line_ptr) \
			+ ', state: ' + str(self.txt[self.line_ptr].get_state_id()) \
			+ ', sbstr state: ' + repr(self.txt[self.line_ptr].get_state_id())
			+ '     ')
		self.menuscrn.addstr(2, 0, 'codec: ' + g_my_codec)
		self.menuscrn.refresh()
		self.menuscrn.leaveok(0)
		self.scrn.move(save_y, save_x)
		return(0)

	def unicode_test(self):
		global g_my_codec

		self.scrn.refresh()
		for j in range(230, 250):
			#self.txt.insert(self.pointasdf, '\u2016') # this character works
			self.txt.insert(self.pointasdf, chr(j))  #chr(j)) #.encode(g_my_codec))
			self.incr_point(1)
			self.display_line()
			self.scrn.refresh()
			time.sleep(.1)
			if j % 40 == 0:
				# insert ocassional line breaks
				self.txt.insert(self.pointasdf, os.linesep)
				self.incr_point(1)
				self.display_line()
				self.scrn.refresh()
		return(0)

	def trace_init(self):
		global g_my_codec, g_trace_dir, TRACE_FNAME

		print_hdr = False
		g_trace_dir = os.path.normpath(os.path.expanduser(g_trace_dir))
		log_fname = os.path.normpath(os.path.expanduser(g_trace_dir \
			+  '/' + TRACE_FNAME))

		if os.access(g_trace_dir, os.F_OK):
			# The target directory exists
			if not os.access(g_trace_dir, os.W_OK):
				# Display error message for the user:
				raise Exception('Write access to trace directory denied: ' \
					+ g_trace_dir)
		else:
			# Target directory does not exist, so create it
			print_hdr = True
			os.mkdir(g_trace_dir)	

		if os.access(log_fname + '2', os.F_OK):
			# the backup log file exists, kill it
			os.remove(log_fname + '2')
		if os.access(log_fname, os.F_OK):
			# rename the previouw log file
			print_hdr = True
			os.rename(log_fname, log_fname + '2')

		header_rec = 'key_nbr|code|win_row|win_col|ibuff_row|ibuff_col|vrow|vcol' \
			+ '|ibuff_len|vbuff_len|iline_pt_start|iline_len|vline_pt_start' \
			+ '|vline_leni\n'

		fdt = codecs.open(log_fname, 'w', g_my_codec)
		if print_hdr:
			fdt.write(header_rec)
		fdt.close
		return(0)

	def trace(self, txt_code, key_nbr=0, a_list=[]):
		'''MainWindow.trace()
		This will send a bunch of debug info to a 
		file. 

		key_nbr  = the numeric value
		           of the key that was most recently pressed.  
		txt_code = a character code reminding you of what the
               trace information represents (10 character max).
		a_list   = a list object that you can pass to display additional
							 stuff.  The entire list must be capable of being 
               displayed with the repr() function (maybe I'll
               do fancier formatting in the future.
		'''
		global g_my_codec, g_trace_dir

		g_trace_dir = os.path.normpath(os.path.expanduser(g_trace_dir))
		log_fname = os.path.normpath(os.path.expanduser(g_trace_dir \
			+  '/' + TRACE_FNAME))

		if os.access(g_trace_dir, os.F_OK):
			# The target directory exists
			if not os.access(g_trace_dir, os.W_OK):
				raise Exception('Write access to trace directory denied: ' \
					+ g_trace_dir)
		else:
			raise Exception('The trace directory disappeared: ' + g_trace_dir)

		format_string = '{0:8d}|{1:10}|{2:4d}|{3:4d}|{4:4d}|{5:4d}' \
			+ '|{6:4d}|{7:4d}|{8:8d}' \
			+ '|{9:6d}|{10:8d}|{11:6d}|{12:8d}|{13:6d}|'
		#out_rec = format_string.format('put debug info here')
		out_rec = 'put debug info here'

		fdt = codecs.open(log_fname, 'a', g_my_codec)
		fdt.write(out_rec)
		fdt.close
		return(0)

	def win_del_char(self, win, y, x):
		# The win.delch(y, x) function appears to be broken: after the first delete
		# it deletes only from that spot, not the new location
		#win.delch(y, x)
		win.delch()
		self.update_status()
		win.refresh()
		return(0)

	def win_del_line(self, win, y):
		pass

	def win_ins_char(self, win, y, x, ch, attr=curses.A_BOLD):
		# insch(y, x, ch, attr)
		win.insch(y, x, ch, attr)
		win.move(y, x+1)
		self.update_status()
		return(0)
########################################################################
def usage():
	print('usage:\ncurses##.py -f filename -c codec')
	print('--verbose')
	print('-v')
	print(' display lots of info about what the program is doing.')
	print('--help')
	print('-h')
	print(' this help message.')
	print('--codec=')
	print('-c CODEC')
	print(' the codec for the input file, such as --codec ISO8859-1')
	print(' or maybe utf8.')
	print('--filename=')
	print('-f FNAME')
	print(' the filename of the text file to edit.')
	print('--trace-dir=')
	print('-t TRACE_DIR')
	print(' the directory to which detailed trace/debug data will ' \
				+ 'be sent.')
def run_curses(window, buff):
	#curses.curs_set(2)#highly visible cursor
	curses.def_shell_mode()
	if curses.has_colors():
		curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
		curses.init_pair(2, curses.COLOR_CYAN, 0)
		curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
		curses.init_pair(4, curses.COLOR_MAGENTA, 0)
		curses.init_pair(5, curses.COLOR_RED, 0)
		curses.init_pair(6, curses.COLOR_YELLOW, 0)
		curses.init_pair(7, curses.COLOR_WHITE, 0)
	w = MainWindow(window, buff) # returns a window object
	w.key_loop()
	return(0)

def main():
	global g_my_codec
	global g_trace_dir

	buff = []
	fname = ''

	try:
		optlist, args = getopt.getopt(sys.argv[1:] \
			,'vhc:f:t:', ['verbose', 'help', 'codec=', 'file=' \
			,'tracedir='])
	except (getopt.GetoptError, err):
		print(str(err))
		usage()
		sys.exit(12)
	#
	for o, a in optlist:
		if (o in ('-h', '--help')):
			usage()
			sys.exit()
		elif (o in ('-v', '--verbose')):
			g_debug_level = 6
			pass
		elif o in ('-c', '--codec'):
			g_my_codec = a
		elif o in ('-f', '--filename'):
			fname = a		
		elif o in ('-t', '--trace-dir'):
			g_trace_dir = a
		#
		# Confirm that a filename was passed.
	if fname == '':
		usage()
		sys.exit()
		#
	fd1 = None
	try:
		fd1 = codecs.open(fname, 'r', g_my_codec)
	except IOError:
		errprint(1, 'Cannot open filename: ' + fname)
		sys.exit(12)
	rows = 0
	# Read the input file
	for s in fd1:
		#buff.append(s.replace('\t', '  '))
		#buff.append(s.replace('\n',chr(0x01)))
		#buff.append(s.replace('\n', 'Q'))
		chunk_count = int((len(s) - 1) / MAX_LRECL) + 1
		for j in range(chunk_count):
			# chop long lines
			buff.append(s[j * MAX_LRECL:MAX_LRECL * (j + 1)])
		rows += 1
	fd1.close

	
	# the following should run from curses.wrapper() but
	# something was wrong
	# filter() is a test to suppress the cursor
	# movement side-effects of displaying EOL
	#curses.filter()
	try:
		#curses.wrapper(run_curses, buff)
		mywrapper(run_curses, buff)
	except:
		traceback.print_exc()

	#
	##curses.reset_shell_mode()
	return(0)

def errprint(code, s):
	print(s)

"""curses.wrapper

Contains one function, wrapper(), which runs another function which
should be the rest of your curses-based application.  If the
application raises an exception, wrapper() will restore the terminal
to a sane state so you can read the resulting traceback.

"""

import curses

def mywrapper(func, *args, **kwds):
	"""This is a modified copy of the curses.wrapper() function
  Wrapper function that initializes curses and calls another function,
	restoring normal keyboard/screen behavior on error.
	The callable object 'func' is then passed the main window 'stdscr'
	as its first argument, followed by any other arguments passed to
	wrapper().
	"""

	res = None
	try:
		# Initialize curses
		stdscr=curses.initscr()
		curses.def_shell_mode()
		curses.noecho()
		curses.cbreak()
		stdscr.keypad(1)

		try:
			curses.start_color()
		except:
			pass

		return func(stdscr, *args, **kwds)
	finally:
		# Set everything back to normal
		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		# I added the def_shell_mode and restore:
		curses.reset_shell_mode()
		curses.endwin()

	# nothing seems to reset the terminal to regular shell mode
	# so I'll run this program from within another shell
	# script that calls my stty repair program after this runs
	#os.system('/usr/bin/fixscreen.sh')

if __name__ == '__main__':
	main()
	
