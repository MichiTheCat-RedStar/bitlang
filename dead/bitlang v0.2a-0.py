#		bitlang // ☭
# MichiTheCat-RedStar (c) 2026

# ПРИЧИНА ОТКАЗА:
# Создание костыльного проссчитывания аргументов через добавление в список выполняемых команд

import re
from os import remove, system

# Тестовый код (Всё ниже до пункта всех типов - тестовая часть, она изменится)
TEST = r'''
print 1;
print 2;
a = "123";
print "aboba";
print! "My age is ";
print! 2077;
print "!!!";
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
	('ВЫВОД', r'print (.*);', 1),
	('ПРИСВОИТЬ', r'([a-zA-Z_]*) = (.*);', 2),
	('ОТОБРАЖЕНИЕ', r'print! (.*);', 1)
]

# Функции файла
def _type(argument) -> tuple:
	'''Проверка типа
	Вывод: tuple(bit_types, тип_без_форматирования)'''
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
		for bit_name, bit_re, bit_args in bit_tokens:
			searched = re.search(bit_re, line)
			if searched:
				if bit_args > 1: # TODO v0.2a костыль, исправить, тут для токенов с большим количеством аргументов второй рассчёт
					for arg in range(bit_args):
						_command_lines.append((bit_name, searched.group(arg+1)))
				else:
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
					elif _arg_type[0] == 'типСТРОКА':
						f.write(f'\tprintf("%s\\n", "{_arg_type[1]}");\n')
				case 'ПРИСВОИТЬ':
					...
				case 'ОТОБРАЖЕНИЕ':
					_arg_type = _type(argument)
					if _arg_type[0] == 'типЧИСЛО':
						f.write(f'\tprintf("%d", {argument});\n')
					elif _arg_type[0] == 'типСТРОКА':
						f.write(f'\tprintf("%s", "{_arg_type[1]}");\n')
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
	variables = {}
	for command, argument in _command_lines:
		match command:
			case 'ВЫВОД':
				print(_type(argument)[1])
			case 'ПРИСВОИТЬ':
				...
			case 'ОТОБРАЖЕНИЕ':
				print(_type(argument)[1], end='')
