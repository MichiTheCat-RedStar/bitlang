#		bitlang // ☭
# MichiTheCat-RedStar (c) 2026

import re
from os import remove, system

# =======[TEST]========================================================
# Тестовый код (Всё ниже до пункта всех типов - тестовая часть, она изменится)
TEST = r'''
print 1;
print 2;
a = "asd123";
print a;
'''
isCompile = False	# Компилировать или интерпретировать?
isDeleteC = False	# Удалять ли файл при компилировании?
Flags = ''			# Флаги
# =====================================================================

# Все типы
bit_types = [ # Хранить регулярки в правильном порядке!
	('типСТРОКА', r'"(.+)"'),
	('типЧИСЛО', r'(\d+)'),
	('типПЕРЕМЕННАЯ', r'([a-zA-Z_]+)')
] # TODO: Вынести в объект класса, чтобы удобнее счиатть тип | <- неудобно будет для переписывания ЯПа на самом себе?

# Все функции
bit_tokens = [ # Хранить регулярки в правильном порядке? Не
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

def _func(line) -> None:
	'''Проверка функции
	Вывод: Изменение _command_lines'''
	#Вывод: tuple(COMMAND, argument|{словарь: "аргумнетов"})''' # <- TODO
	isSearched = False
	for bit_name, bit_re, bit_args in bit_tokens:
		searched = re.search(bit_re, line)
		if searched:
			if bit_args > 1:
				arguments = {}
				for arg in range(bit_args):
					arguments[arg] = searched.group(arg+1)
				_command_lines.append((bit_name, arguments))
			else:
				_command_lines.append((bit_name, searched.group(1)))
			isSearched = True
	if not isSearched:
		raise ValueError(f'Ошибка в строке {_actual_line}!')

# Код в выполняемые последовательно функции
_command_lines = []
_actual_line = 0
for line in TEST.split('\n'):
	if line.strip() != '':
		_func(line)
	_actual_line += 1
del _actual_line # Ну спокойнее мне с явным удалением

print(f'Команды: {_command_lines}\n')

# Выполняемые последовательности в интерпретирование или компилирование
if isCompile:
	print('Компилируется...', end='', flush=True)
	_name = 'tmpBL'+str(hash(TEST))[1:6]+'.c'
	with open(_name, 'a', encoding='utf-8') as f:
		f.write('#include <stdio.h>\n\n#define PRINT(x) printf(_Generic((x), int: "%d", char*: "%s", default: "?"), x)\n\nint main() {\n') # SOF!
		for command, argument in _command_lines:
			match command:
				case 'ВЫВОД':
					_arg_type = _type(argument)
					if _arg_type[0] == 'типЧИСЛО':
						f.write(f'\tprintf("%d\\n", {argument});\n')
					elif _arg_type[0] == 'типСТРОКА':
						f.write(f'\tprintf("%s\\n", "{_arg_type[1]}");\n')
					elif _arg_type[0] == 'типПЕРЕМЕННАЯ':
						f.write(f'\tPRINT({_arg_type[1]}); printf("\\n");\n')
				case 'ПРИСВОИТЬ':
					_arg_type = _type(argument[1])
					if _arg_type[0] == 'типЧИСЛО':
						f.write(f'\tint {_type(argument[0])[1]} = {_arg_type[1]};\n')
					elif _arg_type[0] == 'типСТРОКА':
						f.write(f'\tchar *{_type(argument[0])[1]} = "{_arg_type[1]}";\n')
					elif _arg_type[0] == 'типПЕРЕМЕННАЯ':
						raise TypeError('Нельзя задать переменную в переменную!')
				case 'ОТОБРАЖЕНИЕ':
					_arg_type = _type(argument)
					if _arg_type[0] == 'типЧИСЛО':
						f.write(f'\tprintf("%d", {argument});\n')
					elif _arg_type[0] == 'типСТРОКА':
						f.write(f'\tprintf("%s", "{_arg_type[1]}");\n')
					elif _arg_type[0] == 'типПЕРЕМЕННАЯ':
						f.write(f'\tPRINT({_arg_type[1]});\n')
		f.write('\treturn 0;\n}') # EOF!
	_return = system('gcc '+Flags+_name)
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
				if _type(argument)[0] != 'типПЕРЕМЕННАЯ':
					print(_type(argument)[1])
				else:
					print(variables[(_type(argument)[1])])
			case 'ПРИСВОИТЬ':
				if _type(argument[1])[0] == 'типПЕРЕМЕННАЯ':
					raise TypeError('Нельзя задать переменную в переменную!')
				variables[_type(argument[0])[1]] = _type(argument[1])[1]
			case 'ОТОБРАЖЕНИЕ':
				print(_type(argument)[1], end='')
