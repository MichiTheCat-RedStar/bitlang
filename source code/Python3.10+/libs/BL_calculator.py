#	bitlang/BL_calculator // ☭
# MichiTheCat-RedStar (c) 2026

from BL_tokens import BIT_CALCS # не забыть сменить на относительный путь после успеха

def _glue(bits:list) -> list:
	bit_info = {'NULL':'NULL'}
	result = []
	for bit in bits:
		if bit_info.keys() == bit.keys():
			key = list(bit_info.keys())[0]
			bit_info[key] += bit[key]
		else:
			result.append(bit_info)
			bit_info = bit
	result.pop(0)
	return result

def BL_calculate(text:str) -> list:
	'''Парсер BitLang'''
	
	symbs, bits = list(text), []
	for s in symbs:
		if s != ' ': # continue if ' '
			if s in BIT_CALCS['число']:
				bits.append({'число':s})
			elif s in BIT_CALCS['алгебраическое']:
				bits.append({'алгебраическое':s})
			elif s in BIT_CALCS['логическое']:
				bits.append({'логическое':s})
			elif s in BIT_CALCS['переменная']:
				bits.append({'переменная':s})
			# Код выше можно автоматизировать - нужно
	return _glue(bits)

# TEST | Тест модуля
if __name__ == '__main__':
	_test = 'Aboba = 56 + 3 * 2'
	print(_test, '\n')
	_test = BL_calculate(_test)
	for _ in _test:
		print(_)
