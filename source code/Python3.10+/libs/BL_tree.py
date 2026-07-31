#	bitlang/BL_tree // ☭
# MichiTheCat-RedStar (c) 2026

from .BL_tokens import BIT_TYPES, BIT_TOKENS
import re

def _re_type(text:str) -> dict:
	'''Нахождение типа в тексте
	Получаю строку -> выдаю в ней найденные типы согласно BIT_TYPES
	Находит один конкретный тип в строке:
	 Учёт на то, что будет отправлен один тип и нужно понять какой он'''
	
	for bit_name, bit_re in BIT_TYPES:
		re_search = re.search(bit_re, text.strip())
		if re_search:
			return {'type':bit_name, 'raw':re_search.group(1)}
	raise TypeError('Указан несуществующий тип!')

def _re_function(text:str) -> dict:
	'''Нахождение функции в тексте
	Получаю строку -> выдаю в ней найденные функции согласно BIT_TOKENS
	Находит одну конкретную функцию в строке:
	 Учёт на то, что будет отправлена одна функция и нужно понять какие
	 у неё аргументы и само имя'''
	
	for bit_name, bit_re, bit_args_count in BIT_TOKENS:
		re_search = re.search(bit_re, text)
		
		if re_search:
			searched = [re_search.group(x+1) for x in range(bit_args_count)]
			return {'name':bit_name, 'args':[_re_type(x) for x in searched]}
		
	raise SyntaxError('Указана несуществующая функция!')

def BL_tree(code:str) -> list:
	'''Разбивка токенов на команды для BitLang'''
	
	result = [] # Результатом будет список команд для выолнения
	
	actual_line = 1
	for line in code.split('\n'):
		try:
			line = line.strip()
			
			if line != '':
				result.append(_re_function(line))
			
			actual_line += 1
		except:
			raise SyntaxError(f'Ошибка в строке {actual_line}!\n-> {line}')
	return result

# TEST | Тест модуля
if __name__ == '__main__':
	print(_re_type('"abc"'))
	print(_re_type('123'))
	print(_re_function('print "abc";'))
	print(_re_function('a += 2;'), end='\n\n')
	print(BL_tree('a = 2;\nb = "aboba";\n\nprint! 42;'))
