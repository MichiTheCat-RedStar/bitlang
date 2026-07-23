#		bitlang // ☭
# MichiTheCat-RedStar (c) 2026

import re
from os import remove, system
from libs import *

# =====[ TEST ]========================================================
# Режим ввода кода во время интерпретации вместо исполнения TEST-кода:
REPLmode = True

# Режимы работы:
_settings = {
	'C-code': False,	# Удалять ли C-код?
	'Autorun': False,	# Запускать ли код после компиляции?
	'Flags': ''			# Флаги для gcc (стоит после gcc дял флагов)
}	# Предлагайте свои идеи для добавления настроек!

# На случай, если REPLmode == False:
_bl_code = '''
print "Привет, BitLnag!";
name = "Иванов";
age = 42;
print! "Имя: ";
print! name;
print! ", возраст: ";
print! age;
print "."
age += 38;
age -= 20;
print age;
'''.strip() # .strip() для того, чтобы писать между 0 и -1 строкой TEST

if REPLmode: # Работа с libs/BL_REPL
	REPL_result = BL_REPL()
	_settings = REPL_result['settings']
	_bl_code = REPL_result['result_code']
	if REPL_result['exitcode']: quit()
	del REPL_result # Явное удаление для успокоения
# =====================================================================

# Добавление пробела в флаги gcc, если он не стоит
_settings['Flags'] = _settings['Flags'].strip()
if len(_settings['Flags']) > 0: _settings['Flags'] += ' '
# TODO: print('gcc '+_settings['Flags']+'пукпук.bl') Оставить не тут, а перекинуть в конец
