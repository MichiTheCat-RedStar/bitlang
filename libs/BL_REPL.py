#	bitlang/BL_REPL // ☭
# MichiTheCat-RedStar (c) 2026

def _yes_no(text:str) -> bool:
	'''Вопросы с ответом Y/N'''
	# Yes и No должны быть в нижнем регистре
	Yes = ['y', 'yes', 'yeah', 'oh yeah', 'да', 'д', 'конечно', 'давай']
	No = ['n', 'no', 'nope', 'нет', 'н', 'не-а', 'никогда', 'нигативно']
	while True:
		user = input(text).lower().strip()
		if user in Yes:
			return True
		elif user in No:
			return False
		else:
			print('Направильный ввод!\n')

def BL_REPL() -> dict:
	'''REPL для BitLang'''
	
	result = { # return result
		'settings': {'C-code':False, 'Autorun':False, 'Flags':''}, # _settings = settings
		'result_code': '', # _bl_code = result_code
		'exitcode': False, # if exitcode: quit()
		'save': False # TODO for v0.3a+
	}
	
	print('BitLang - MichiTheCat-RedStar (c) 2026.',
	'\nНапишите /run для запуска или /exit для выхода без сохранения.\n')
	
	while True:
		match _input := input('> '):
			case '/exit':
				print('\nУдачного Вам дня, вечера или ночи!')
				result['exitcode'] = True
				return result
			case '/run':
				print()
				if _yes_no('Оставить C-code? (Y/N): '):
					result['settings']['C-code'] = True
				if _yes_no('Запустить код при успешкой компиляции? (Y/N): '):
					result['settings']['Autorun'] = True
				result['settings']['Flags'] = input('Укажите флаги для gcc компиляции, если их нет, просто нажмите Enter: ')
				return result
			case _:
				result['result_code'] += _input+'\n'

# TEST | Тест модуля
if __name__ == '__main__':
	print('\n', BL_REPL())
