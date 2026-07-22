#		bitlang // ☭
# MichiTheCat-RedStar (c) 2026

import re
from os import remove, system

# Тестовый код
TEST = '''
print 1;
print 2;
a = "123";
print "aboba";
'''
isCompile = False	# Компилировать или интерпретировать?
isDeleteC = False	# Удалять ли файл при компилировании?
# TODO: Пока можно выводить только числа (уже и строки) и только выводить - начал с
# малого, а в дальнейшем будет разбивание на типы данных и прочее...

# Все типы
bit_types = [
	('типЧИСЛО', r'(\d+)'),
	('типСТРОКА', r'"(.+)"')
	# типПЕРЕМЕННАЯ
]

# Все функции
bit_tokens = [
	('ВЫВОД', r'print (.*);'),
	('ПРИСВОИТЬ', r'([a-zA-Z_]*) = (.*?);') # TODO
]

# Функции файла
def _type(argument) -> tuple:
	'''Проверка типа'''
	for bit_name, bit_re in bit_types:
		searched = re.search(bit_re, argument)
		if searched:
			return ((bit_name, searched.group(1)))
	else:
		raise TypeError('Ошибка типа!')

# Код в выполняемые последовательно функции
_command_lines = []
_actual_line = 0
for line in TEST.split('\n'):
	if line.strip() == '':
		_actual_line += 1
		continue
	else:
		isSearched = False
		for bit_name, bit_re in bit_tokens:
			searched = re.search(bit_re, line)
			if searched:
				_command_lines.append((bit_name, searched.group(1)))
				isSearched = True
		if not isSearched:
			_actual_line = 'Ошибка в строке '+str(_actual_line)+'!'
			raise ValueError(_actual_line)
	_actual_line += 1
del _actual_line

print(f'Команды: {_command_lines}\n')

# Выполняемые последовательности в интерпретирование или компилирование
if isCompile:
	print('Компилируется...', end='', flush=True)
	_name = 'tmpBL'+str(hash(TEST))[1:6]+'.c'
	with open(_name, 'a', encoding='utf-8') as f:
		f.write('#include <stdio.h>\n\nint main() {\n') # SOF!
		for command, argument in _command_lines:
			match command:
				case 'ВЫВОД':
					_arg_type = _type(argument)
					if _arg_type[0] == 'типЧИСЛО':
						f.write(f'\tprintf("%d\\n", {argument});\n')
					else: # <- Пока только два типа (Число и Строка) работает, но в будущем перепишу
						argument = _arg_type[1]
						f.write(f'\tprintf("{argument}\\n");\n')
				case 'ПРИСВОИТЬ':
					...
		f.write('\treturn 0;\n}') # EOF!
	_return = system('gcc '+_name)
	if isDeleteC:
		remove(_name)
	if _return == 0:
		print('\rВсё скомпилированно!')
	else:
		print('\rЗавершено с кодом:', _return)
else:
	print('Интерпретация:')
	for command, argument in _command_lines:
		match command:
			case 'ВЫВОД':
				print(_type(argument)[1])
			case 'ПРИСВОИТЬ':
				...
