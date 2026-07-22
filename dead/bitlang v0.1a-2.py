#		bitlang // ☭
# MichiTheCat-RedStar (c) 2026

import re
from os import remove, system

# Тестовый код
TEST = '''
print_int 1;
print_int 2;
print_str asd;
'''
isCompile = True	# Компилировать или интерпретировать?
isDeleteC = False	# Удалять ли файл при компилировании?
# TODO: Пока можно выводить только числа и только выводить - начал с
# малого, а в дальнейшем будет разбивание на типы данных и прочее...

# Все функции
bit_tokens = [
	('ВЫВОД_ЧИСЛО', r'print_int (.*?);'),
	('ВЫВОД_СТРОКА', r'print_str (.*?);')
]

# Код в выполняемые последовательно функции
_command_lines = []
for line in TEST.split('\n'):
	for bit_name, bit_re in bit_tokens:
		searched = re.search(bit_re, line)
		if searched:
			_command_lines.append((bit_name, searched.group(1)))

print(f'Команды: {_command_lines}\n')

# Выполняемые последовательности в интерпретирование или компилирование
if isCompile:
	print('Компилируется...', end='', flush=True)
	_name = 'tmpBL'+str(hash(TEST))[1:6]+'.c'
	with open(_name, 'a', encoding='utf-8') as f:
		f.write('#include <stdio.h>\n\nint main() {\n') # SOF!
		for command, argument in _command_lines:
			match command: # COMMANDS
				case 'ВЫВОД_ЧИСЛО':
					f.write(f'\tprintf("%d\\n", {argument});\n')
				case 'ВЫВОД_СТРОКА':
					f.write(f'\tprintf("{argument}\\n");\n')
		f.write('\treturn 0;\n}') # EOF!
	_return = system('gcc '+_name)
	if isDeleteC:
		remove(_name)
	if _return == 0:
		print('\rВсё скомпилированно!')
	else:
		print('\rЗавершено с кодом:', _return)
else:
	print('Интерпретация:\n')
	for command, argument in _command_lines:
		match command:
			case 'ВЫВОД_ЧИСЛО':
				print(argument)
			case 'ВЫВОД_СТРОКА':
				print(argument)
