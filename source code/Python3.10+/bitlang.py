#		bitlang // ☭
# MichiTheCat-RedStar (c) 2026

from libs import BL_REPL, BL_tree, BL_compile
from os import system, name as os_name
from sys import argv

# =====[ TEST ]========================================================
# Режим ввода кода во время интерпретации вместо исполнения TEST-кода:
REPLmode = True

# Режимы работы:
_settings = {
	'C-code': True,		# Оставить ли C-код?
	'Autorun': True,	# Запускать ли код после компиляции?
	'Flags': '-std=c11'	# Флаги для gcc (стоит после gcc дял флагов)
}	# Предлагайте свои идеи для добавления настроек!

# На случай, если REPLmode == False:	// В основном для тестов
_bl_code = r'''
// Напишите здесь свой код для теста
a = 5;
print! "Введите число и оно отобразится: ";
input a;
print! "\nВот ваше число: ";
print a;
// Он будет скомпилирован и запущен!
'''.strip() # .strip() для того, чтобы писать между 0 и -1 строкой TEST

if REPLmode and len(argv)<2: # Работа с libs/BL_REPL
	REPL_result = BL_REPL()
	if REPL_result['exitcode']: quit()
	_settings = REPL_result['settings']
	_bl_code = REPL_result['result_code']
	_save = REPL_result['save']
	print()
else:
	_save = False
	print(_bl_code+'\n')
# =====================================================================

if __name__ == '__main__':
	if len(argv)<2:
		if _save:
			with open('a.bl', 'w', encoding='utf-8') as f:
				f.write(_bl_code)
		_bl_tree_code = BL_tree(_bl_code)
		print('Компилируется...', end='', flush=True)
		if (ErrCode := BL_compile(_bl_tree_code, _settings)) == 0:
			print('\rУспешная компиляция!\n')
			if _settings['Autorun']:
				print('--- BitLang Autorun ---')
				if os_name == 'nt':
					system('a.exe')
				else:
					system('./a.out')
		else:
			print('\rОшибка компиляции! Код:', ErrCode)
	else:
		try:
			with open(argv[1], 'r', encoding='utf-8') as f:
				_bl_code = f.read()
		except FileNotFoundError:
			raise FileNotFoundError('Файл не найден!')
		_settings = {'C-code':False, 'Autorun':False, 'Flags':'-std=c11'}
		_bl_tree_code = BL_tree(_bl_code)
		if (ErrCode := BL_compile(_bl_tree_code, _settings)) == 0:
			print('\rУспешная компиляция!\n')
		else:
			print('\rОшибка компиляции! Код:', ErrCode)
