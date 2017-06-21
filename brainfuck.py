# brainfuck.py
# By: Nostro Vostro aka. Trevor LeCroy
# You can contact me via email:
# trevor_lecroy@programmer.net
# www.twomendrinkingcoffee.com
#
#
# The goal of this was to give Brainfuck some addtional
# functionality whether it actually does anything or not
# Either way, I learned quite a lot about interpreters
# whilst creating this.
#
#
# Usage: 
# python brainfuck.py [file name]
# or for the live interpreter
# python brainfuck.py --live
# You may also include a -h at the end of 
# those to hide the output of cells when
# the program finishes execution
#
#
# Brainfuck with a few added features
# Including a live interpreter
# Additional non-vanilla Brainfuck comamnds:
# 	^ - multiplies the current cell by itself
# 	@ - sets the current cell to 0
# 	! - removes the current cell
#  $> - copys the current cell to the right
#  $< - copys the current cell to the left
#	
#  if statements! Here's how they work:
#	use ? with either <, >, or = to compare if the current cell 
#   is greater, less than, or equal to the cell before this one. 
#   after ? and <, >, or =, use { } and put the conditioned code 
#   inside of the braces.
#   Here's a quick example:
#   	++++ > +++++ ? < { > +++ [>++<-] }
#	Whats happening:
#	The first cell is set to 4, then the pointer moves over 1
#   5 second cell is set to 5, then comes our conditional
#   We want to see if the our cell is greater than the one
#   prior to it, in this case, our current cell is greater than
#   the last, so it will run the code in the curly braces.
#   
#   In the future I'd like to make if statements a little more 
#   intuitive, and allow for more comparisons against cells in 
#   different locations other than the one prior to the current one.
#
#  These are all probably pretty useless features, but oh well
#  they were fun to add either way.
import sys

interpreter = None

class Interpreter():

	def __init__(self, hide_cell_output):
		self.hide_cell_output = hide_cell_output

	# This function prints out all cells, and
	# will display what cell the program ended on
	def print_cells(self, cells, cell_ptr):
		if not self.hide_cell_output:
			txt = '('
			for i, cell in enumerate(cells):
				if i == cell_ptr:
					txt += '[{}]'.format(cell)
				else:
					txt += '{}'.format(cell)
				
				if i != len(cells)-1:
					txt += ', '

			txt += ')'
			print('\n -> ' + txt)

	def create_cbracearray(self, text):
		_braces, braces = [], {}

		for i, command in enumerate(text):
			if command == '{':
				_braces.append(i)
			elif command == '}':
				start = _braces.pop()

				braces[start] = i
				braces[i]     = start
				
		# print(braces.keys())
		# print(braces.values())
		return braces

	def create_bracearray(self, text):
		# Setup a list, and dict for 
		# all braces in our user's code
		_braces, braces = [], {}
		# Interate over our user's code
		for i, command in enumerate(text):
			# If the current character is 
			# equal to [ then we want to 
			# add the position into a stack
			if command == '[':
				_braces.append(i)
			# If the current character is
			# equal to ] then we want to
			# know the position of both
			# the [ and ] so we know where
			# to send our code to during the
			# iteration loop
			elif command == ']':
				# We use a try catch just incase
				# Our user happens to put a ] but not [
				try:
					start = _braces.pop()

					braces[start] = i
					braces[i]     = start
				except IndexError:
					print('Syntax Error: Invalid syntax')
		return braces

	def parse(self, text, text_ptr, cells, cell_ptr, braces, cbraces):
		# While the current text position is less than the length
		# of all of our user's code, we want to see the current 
		# character we're on, and if it's a command, we want to
		# execute that command
		try:
			while text_ptr < len(text):
				cmd = text[text_ptr]

				if cmd == '>':
					cell_ptr += 1
					if cell_ptr == len(cells): cells.append(0)
				
				if cmd == '<':
					cell_ptr = 0 if cell_ptr <= 0 else cell_ptr - 1

				if cmd == '+':
					cells[cell_ptr] += 1
				
				if cmd == '-':
					cells[cell_ptr] -= 1

				if cmd == '^':
					cells[cell_ptr] = cells[cell_ptr] * cells[cell_ptr] 
					if cells[cell_ptr] > 127:
						cells[cell_ptr] = 127

				if cmd == '@':
					cells[cell_ptr] -= cells[cell_ptr]

				if cmd == '[' and cells[cell_ptr] == 0:
					text_ptr = braces[text_ptr]

				if cmd == ']' and cells[cell_ptr] != 0:
					text_ptr = braces[text_ptr]

				if cmd == '!' and len(cells) > 1:
					cells.pop(cell_ptr)
					if cell_ptr > len(cells) - 1: cell_ptr -= 1
				
				if cmd == '?' and text_ptr + 2 in cbraces:

					if cell_ptr < len(cells) - 1:
						continue

					#print('If statement')
					if text[text_ptr + 1] == '>' and cells[cell_ptr - 1] > cells[cell_ptr]:
						#print('Greater than')
						text_ptr = cbraces[cbraces[text_ptr + 2]]
					elif text[text_ptr + 1] == '<' and cells[cell_ptr - 1] < cells[cell_ptr]:
						#print('Less than')
						text_ptr = cbraces[cbraces[text_ptr + 2]]
					elif text[text_ptr + 1] == '=' and cells[cell_ptr] == cells[cell_ptr - 1]:
						#print('Equal')
						text_ptr = cbraces[cbraces[text_ptr + 2]]
						#print('Going to {}'.format(text_ptr + 2))
					else:
						#print('None, skipping')
						text_ptr = cbraces[text_ptr + 2]

				if cmd == '$':
					#print('Copy')
					#print(text[text_ptr + 1])
					#print(cell_ptr)
					#print(len(cells))
					if text[text_ptr + 1] == '>':
						if cell_ptr + 1 == len(cells):
							cells.append(0)

						#print('Copy Right')
						#print(cell_ptr + 1)
						#print(cells)
						cells[cell_ptr + 1] = cells[cell_ptr] 
						text_ptr += 1
					elif text[text_ptr + 1] == '<' and cell_ptr != 0:
						#print('Copy Left')
						cells[cell_ptr - 1] = cells[cell_ptr] 
						text_ptr += 1 

				if cmd == '.':
					if cells[cell_ptr] <= 127:
						print(chr(cells[cell_ptr]), end='')
					else:
						print('\nEncoding Error: {} in cell {} does not map to a Ascii character!'.format(cells[cell_ptr], cell_ptr))
					
				if cmd == ',':
					inp = input(' ')
					if len(inp) >= 1:
						cells[cell_ptr] = ord(inp[0]) 

				text_ptr += 1
		except(KeyboardInterrupt, EOFError):
			print('\n\n\nFinished.')
		return cells, cell_ptr

	def main(self, f_name):
		live_console = False
		text = ''

		if f_name == '--live':
			live_console = True
		elif f_name != '--live':
			# Open our file
			file = open(f_name, 'r')
			# Read all the text in our file
			# into a list
			text = list(file.read())
			for i, element in enumerate(text):
				if element == ' ':
					text.pop(i)

			# Close our file
			file.close()

		# Initialize some variables we'll need
		cells    = [0]
		cell_ptr = 0
		text_ptr = 0

		# If we're running the live
		# interpreter, then we'll go into
		# an input loop, otherwise, we'll 
		# loop over the file that was input
		if live_console:
			try:
				while live_console:
					text = input('->: ')
					braces          = self.create_bracearray(text)
					cbraces         = self.create_cbracearray(text)
					cells, cell_ptr = self.parse(text, text_ptr, cells, cell_ptr, braces, cbraces)
					self.print_cells(cells, cell_ptr)

			except (EOFError, KeyboardInterrupt):
				print('\n\n\nFinished')
		else:
			# We want to get the locaiton of all of
			# our braces first
			braces          = self.create_bracearray(text)
			cbraces         = self.create_cbracearray(text)
			# We want to parse the file next
			cells, cell_ptr = self.parse(text, text_ptr, cells, cell_ptr, braces, cbraces)
			# After parsing, and execution,
			# we want to print out all of our cells
			# and display the one we ended on
			self.print_cells(cells, cell_ptr)

	def file_output(self, file):
		pass


# Is this the file being ran?
# If so, then execute this
if __name__ == '__main__':
	# I'll be switching this over
	# to argparse soon. Just doing this
	# for now, because I'm pretty lazy.
	f_name           = sys.argv[1]
	hide_cell_output = False
	if len(sys.argv) > 2:
		hide_cell_output = sys.argv[2] 
	
	if hide_cell_output == '-h':
		hide_cell_output = True
	else:
		hide_cell_output = False


	interpreter = Interpreter(hide_cell_output)

	interpreter.main(f_name)