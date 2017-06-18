# brainfuck.py
# By: Nostro Vostro aka. Trevor LeCroy
# You can contact me via email:
# trevor_lecroy@programmer.net
# www.twomendrinkingcoffee.com
#
#
# Usage: 
# python brainfuck.py [filename]
# or for the live interpreter
# python brainfuck.py --live
#
#
# Brainfuck with a few added features
# Including a live interpreter
# Additional non-vanilla Brainfuck comamnds:
# 	^ - multiplies the current cell by itself
# 	@ - sets the current cell to 0
# 	! - removes the current cell
import sys

# This function prints out all cells, and
# will display what cell the program ended on
def print_cells(cells, cell_ptr):
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

def create_bracearray(text):
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

def parse(text, text_ptr, cells, cell_ptr, braces):
	# While the current text position is less than the length
	# of all of our user's code, we want to see the current 
	# character we're on, and if it's a command, we want to
	# execute that command
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
			
		if cmd == '.':
			print(chr(cells[cell_ptr]), end='')
			
		if cmd == ',':
			inp = input(' ')
			if len(inp) >= 1:
				cells[cell_ptr] = ord(inp[0]) 

		text_ptr += 1
	return cells, cell_ptr

def main(f_name):
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
				braces          = create_bracearray(text)
				cells, cell_ptr = parse(text, text_ptr, cells, cell_ptr, braces)
				print_cells(cells, cell_ptr)

		except (EOFError, KeyboardInterrupt):
			print('\n\n\nFinished')
	else:
		# We want to get the locaiton of all of
		# our braces first
		braces          = create_bracearray(text)
		# We want to parse the file next
		cells, cell_ptr = parse(text, text_ptr, cells, cell_ptr, braces)
		# After parsing, and execution,
		# we want to print out all of our cells
		# and display the one we ended on
		print_cells(cells, cell_ptr)

# Is this the file being ran?
# If so, then execute this
if __name__ == '__main__':
	# Look for terminal arguments
	# In our case, we're looking for
	# a file name, or for --live
	f_name = sys.argv[1]
	main(f_name)