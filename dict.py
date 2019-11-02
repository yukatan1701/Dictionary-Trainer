import random
import argparse
import sys

def please():
	print('->', end = ' ')

def try_again(text):
	print(text + '. Please try again.')
	please()

def load_dictionary(filename):
	d = {}
	f = open(filename, 'r')
	for line in f:
		eng, rus = list(line.split(','))
		eng_set = frozenset(eng.split(dict_sep))
		rus_set = frozenset(rus[:-1].split(dict_sep))
		d[eng_set] = rus_set
	f.close()
	return d

def clear(s):
	new = ''
	for char in s:
		if char.isalpha() or char == ' ':
			new += char
	return new
	
def set_to_str(s, size = 'normal'):
	line = ''
	if size == 'normal':
		arr = [x for x in s]
	elif size == 'upper':
		arr = [x.upper() for x in s]
	elif size == 'lower':
		arr = [x.lower() for x in s]
	line += arr[0]
	if len(arr) > 1:
		line += ' ('
	for i in range(1, len(arr)):
		line += arr[i]
		if i < len(arr) - 1:
			line += ', '
	if len(arr) > 1:
		line += ')'
	return line
	
def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', type=str, help='Training mode: \
		0 or %s - mixed, 1 or %s - [rus->eng], 2 or %s - [eng->rus]' % \
		(modes), choices=['0', '1', '2'] + list(modes))
	return parser.parse_args()
	
def get_lower_set(s):
	return frozenset([x.lower() for x in s])
	
def training():
	print()
	print((MAGENTA + 'Let\'s start! (mode: %s)' + RESET) % (modes[mode]))
	right = 0
	wrong = 0
	# the 5 words last used with its translations
	LAST_SIZE =  len(d) // 3 * 2 if len(d) > 10 else 5
	last_used = []
	leave_command = 'end()'
	while True:
		# 1: rus-eng, 2: eng-rus
		local_mode = mode
		# mixed mode
		if mode == 0:
			local_mode = random.randint(1, 2)
		
		if local_mode == 2:
			one, two = random.choice(list(d.items()))
		else:
			two, one = random.choice(list(d.items()))
		if one in last_used:
			continue
		else:
			if len(last_used) == LAST_SIZE:
				last_used = last_used[2:]
				last_used.append(one)
			else:
				last_used.append(one)
			last_used.append(two)
		print(YELLOW + '-> ' + set_to_str(one) + RESET)
		please()
		comp = input()
		if comp in quit_commands:
			leave_command = 'exit()'
			break
		elif comp == 'menu()':
			leave_command = 'menu()'
			break
		elif comp == 'end()':
			leave_command = 'end()'
			break
		comp = clear(comp)
		if comp.lower() not in get_lower_set(two):
			wrong += 1
			print("No, it's " + set_to_str(two, 'upper'))
		else:
			right += 1
		print()
	print(("\n%sRight:%s %d\n%sWrong:%s %d\n") \
		% (GREEN, RESET, right, RED, RESET, wrong))
	if leave_command == 'exit()':
		exit()
	elif leave_command == 'menu()':
		menu()
	elif leave_command == 'end()':
		actions = ('0', '1', '2', 'menu', 'restart', 'exit')
		print('Choose the next action: 0 - menu, 1 - restart, 2 - exit')
		please()
		command = input()
		while command not in actions:
			try_again('Unknown command')
			command = input()
		if command == '0' or command == 'menu':
			menu()
		elif command == '1' or command == 'restart':
			training()
		elif command == '2' or command == 'exit':
			exit()

def set_to_file_str(s):
	words = list(s)
	line = words[0]
	for i in range(1, len(words)):
		line += dict_sep + words[i]
	return line

def add_word():
	print()
	print('Use comma to add pair: eng_word_1/eng_word_n,rus_word_1/rus_word_n')
	commands = ('end()', 'del()')
	all_commands = commands + quit_commands
	new_words = {}
	line = ''
	while True:
		print(YELLOW + '[Add]' + RESET + '->', end = ' ')
		line = input()
		if line in commands or line in quit_commands:
			break
		pair = line.split(',')
		if len(pair) != 2:
			print('Incorrect pair syntax.')
		else:
			eng = frozenset(pair[0].split(dict_sep))
			rus = frozenset(pair[1].split(dict_sep))
			has_eng = eng in d.keys()
			has_rus = rus in d.values()
			if not has_eng and not has_rus:
				new_words[eng] = rus
				d[eng] = rus
				f = open(words_file, 'a+')
				f.write('%s,%s\n' % (set_to_file_str(eng), set_to_file_str(rus)))
				f.close()
				print('Word was added to dictionary.')
			else:
				if has_eng:
					word = eng
				if has_rus:
					word = rus
				print("Word '%s' has already exists. Skipped." % (set_to_file_str(word)))
	
	cmd = line
	if cmd == 'end()':
		change_dictionary()
	elif cmd == 'del()':
		delete_word()
	elif cmd in quit_commands:
		exit()
	
	
def delete_word():
	return
	print()
	print('Enter english or russian word to delete.')
	commands = ('end()', 'add()')
	all_commands = commands + quit_commands
	new_words = {}
	line = ''
	while True:
		print(LRED + '[Delete]' + RESET + '->', end = ' ')
		line = input()
		if line in commands or line in quit_commands:
			break
		
		has_eng = line in d.keys()
		has_rus = line in d.values()
		if not has_eng and not has_rus:
			print('Cannot find word in the dictonary.')
		else:
			full_line = ''
			if has_eng:
				word = eng
			if has_rus:
				word = rus
			print("Word '%s' has already exists. Skipped." % (word))
	
	cmd = line
	if cmd == 'end()':
		change_dictionary()
	elif cmd == 'del()':
		delete_word()
	elif cmd in quit_commands:
		exit()

def change_dictionary():
	print()
	print(MAGENTA + 'Change dictionary:' + RESET)
	print('> add word [add]')
	print('> delete word [del]')
	print('> back to menu [menu]')
	print()
	commands = ('add', 'del', 'menu')
	please()
	command = input()
	while command not in commands and command not in quit_commands:
		try_again('Unknown command')
		command = input()
	if command in quit_commands:
		exit()
	elif command == 'add':
		add_word()
	elif command == 'del':
		delete_word()
	elif command == 'menu':
		menu()

def choose_mode():
	print()
	print('Choose training mode:')
	print(('> 0 or %s - Mixed mode\n> 1 or %s - Russian to English\n' + 
		'> 2 or %s - English to Russian') % modes)
	please()
	text_mode = input()
	if text_mode == '':
		text_mode = '0'
	while text_mode not in all_modes:
		if text_mode in quit_commands:
			quit()
		try_again('Invalid mode')
		text_mode = input()
	global mode
	if all_modes.index(text_mode) > 2:
		mode = int(all_modes.index(text_mode) % len(modes))
	else:
		mode = int(text_mode)
	print("Mode: ", mode)
	training()

def exit():
	quit()

def menu():
	print()
	print(MAGENTA + 'Menu:' + RESET)
	menu_commands = ('start', 'change')
	print('> start training [start]')
	print('> change dictionary [change]')
	print()
	please()
	command = input()
	while command not in menu_commands and command not in quit_commands:
		try_again('Unknown command')
		command = input()
	if command == 'start':
		choose_mode()
	elif command == 'change':
		change_dictionary()
	elif command in quit_commands:
		exit()
	
YELLOW = '\033[0;33m'
LRED = '\033[0;31m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
RESET = '\033[0m'

dict_sep = '/'
quit_commands = ('*', 'quit()', 'exit()')
modes = ('mixed', 'ruseng', 'engrus')
all_modes = ('0', '1', '2') + modes
mode = 0
words_file = 'words.txt'
d = load_dictionary(words_file)
args = get_args()
arg_count = len(sys.argv) - 1
if arg_count > 0:
	mode = args.mode
	if all_modes.index(mode) > 2:
		mode = int(all_modes.index(mode) % len(modes))
	else:
		mode = int(mode)
	training()
else:
	print(YELLOW + "[Help] " + RESET + "Input '*', 'exit()' or 'quit()' " + \
		"if you want to exit.")
	print(CYAN + '< Welcome to the dictionary! >' + RESET)
	menu()

