#	bitlang/BL_compiler // ☭
# MichiTheCat-RedStar (c) 2026

from os import remove, system

DEFAULT = r'''
// Создано с помощью BitLang | Created with BitLang
// BitLang from MichiTheCat-RedStar (c) 2026.
// https://github.com/MichiTheCat-RedStar/bitlang

#include <stdio.h>
#include <locale.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#define bit_print_raw(x) printf(_Generic((x), int: "%d", char*: "%s", bool: "%d", default: "?"), x)
#define bit_print_new(x) printf(_Generic((x), int: "%d\n", char*: "%s\n",  bool: "%d\n", default: "?"), x)

int main() {
	
	char *locale = setlocale(LC_ALL, "");
	srand((unsigned int)time(NULL));
	
	// === User Code Part ===
	<|BL-USERCODE|>
	// ======================
	
	return 0;
}
'''.strip()

def BL_compile(tree_code:list, settings:dict) -> str: # TODO: функцию разбить как минимум на правильный транслитор и саму компиляцию
	'''Компиляция BitLang'''
	
	flags = settings['Flags']
	
	flags = flags.strip() # работа с gcc {flags} file.c
	if len(flags) > 0: flags += ' '
	
	variables = {} # {name:type} // Я сейчас ужасно сонный и творю такие банальные ошибки.. у меня была бессонная ночь, поэтому это меньшее, что я могу сделать - в будущем это будет исопользоваться не только в ПРИСВОИТЬ
	result = [] # Транслирование
	for command in tree_code:
		name, args = command['name'], command['args']
		#print(name, args)
		
		match name:								# result.append(f'*;')
			case 'ВЫВОД': # TODO отказаться от case в пользу поддержки Python <3.10?
				if args[0]["type"] == 'типСТРОКА':
					result.append(f'bit_print_new("{args[0]["raw"]}");')
				else:
					result.append(f'bit_print_new({args[0]["raw"]});')
			
			case 'ОТОБРАЖЕНИЕ':
				if args[0]["type"] == 'типСТРОКА':
					result.append(f'bit_print_raw("{args[0]["raw"]}");')
				else:
					result.append(f'bit_print_raw({args[0]["raw"]});')
			
			case 'ПРИСВОИТЬ': # TODO надеюсь всё работает, я ужасно сонный
				if args[0]["raw"] in variables.keys():
					if (args[1]["type"] == 'типСТРОКА') and (variables[args[0]["raw"]] == 'типСТРОКА'):
						result.append(f'{args[0]["raw"]} = "{args[1]["raw"]}";')
						variables[args[0]["raw"]] = args[1]["type"]
					elif (args[1]["type"] == 'типЧИСЛО') and (variables[args[0]["raw"]] == 'типЧИСЛО'):
						result.append(f'{args[0]["raw"]} = {args[1]["raw"]};')
						variables[args[0]["raw"]] = args[1]["type"]
					elif (args[1]["type"] == 'типПЕРЕМЕННАЯ') and (variables[args[0]["raw"]] == 'типПЕРЕМЕННАЯ'):
						result.append(f'{args[0]["raw"]} = {args[1]["raw"]};')
						variables[args[0]["raw"]] = args[1]["type"]
					elif (args[1]["type"] == 'типБУЛЕВО') and (variables[args[0]["raw"]] == 'типБУЛЕВО'):
						result.append(f'{args[0]["raw"]} = {args[1]["raw"]};')
						variables[args[0]["raw"]] = args[1]["type"]
					else:
						raise TypeError('Указан неверный тип!')
				else:
					if args[1]["type"] == 'типСТРОКА':			# строка
						result.append(f'char *{args[0]["raw"]} = "{args[1]["raw"]}";')
						variables[args[0]["raw"]] = args[1]["type"]
					elif args[1]["type"] == 'типЧИСЛО':			# число
						result.append(f'int {args[0]["raw"]} = {args[1]["raw"]};')
						variables[args[0]["raw"]] = args[1]["type"]
					elif args[1]["type"] == 'типПЕРЕМЕННАЯ':	# переменная
						result.append(f'{args[0]["raw"]} = {args[1]["raw"]};')
						variables[args[0]["raw"]] = args[1]["type"]
					elif args[1]["type"] == 'типБУЛЕВО':		# булево
						result.append(f'bool {args[0]["raw"]} = {args[1]["raw"]};')
						variables[args[0]["raw"]] = args[1]["type"]
			
			case 'КОММЕНТАРИЙ':
				continue
			
			case 'ПРИБАВИТЬ':
				if (args[0]["type"] == 'типПЕРЕМЕННАЯ') and (args[1]["type"] == 'типЧИСЛО'):
					result.append(f'{args[0]["raw"]} += {args[1]["raw"]};')
				else:
					raise TypeError('Указан неверный тип! Должно быть прибавление к переменной числа!')
			
			case 'ОТНЯТЬ':
				if (args[0]["type"] == 'типПЕРЕМЕННАЯ') and (args[1]["type"] == 'типЧИСЛО'):
					result.append(f'{args[0]["raw"]} -= {args[1]["raw"]};')
				else:
					raise TypeError('Указан неверный тип!  Должно быть вычитание из переменной числа!')
			
			case 'УМНОЖИТЬ':
				if (args[0]["type"] == 'типПЕРЕМЕННАЯ') and (args[1]["type"] == 'типЧИСЛО'):
					result.append(f'{args[0]["raw"]} *= {args[1]["raw"]};')
				else:
					raise TypeError('Указан неверный тип! Должно быть прибавление к переменной числа!')
			
			case 'РАЗДЕЛИТЬ':
				if (args[0]["type"] == 'типПЕРЕМЕННАЯ') and (args[1]["type"] == 'типЧИСЛО'):
					result.append(f'{args[0]["raw"]} /= {args[1]["raw"]};')
				else:
					raise TypeError('Указан неверный тип! Должно быть вычитание из переменной числа!')
			
			case 'ОСТАТОК':
				if (args[0]["type"] == 'типПЕРЕМЕННАЯ') and (args[1]["type"] == 'типЧИСЛО'):
					result.append(f'{args[0]["raw"]} %= {args[1]["raw"]};')
				else:
					raise TypeError('Указан неверный тип! Должно быть вычитание из переменной числа!')
			
			case 'УСЛОВИЕ':
				result.append(f'if ({args[0]["raw"]}) '+'{')
			
			case 'УСЛОВИЕИНАЧЕ':
				result.append('}'+f' elif ({args[0]["raw"]}) '+'{')
			
			case 'ЦИКЛ':
				result.append(f'while ({args[0]["raw"]}) '+'{')
			
			case 'ПОДСЧЁТ':
				if (args[0]["type"] == 'типПЕРЕМЕННАЯ') and (args[1]["type"] == 'типЧИСЛО'):
					result.append(f'for (int {args[0]["raw"]} = 0; i < {args[1]["raw"]}; ++{args[0]["raw"]}) '+'{')
				else:
					raise TypeError('Указан неверный тип! Должны быть переменная и число!')
			
			case 'ИНАЧЕ':
				result.append('} else {')
			
			case 'КОНЕЦУСЛОВИЯ':
				result.append('}')
			
			case 'ЗАДАТЬ':
				# result.append('printf("> ");')
				if args[0]["type"] == 'типПЕРЕМЕННАЯ':
					result.append(f'scanf("%d", &{args[0]["raw"]});')
				else:
					raise TypeError('Указан неверный тип! Должна быть переменная!')
			
			case 'ИМПОРТ-СИ':
				if args[0]["type"] == 'типСТРОКА':
					try:
						with open(args[0]['raw'], 'r') as f:
							data = f.read()
						data = data.split('\n')
						result += data
					except FileNotFoundError:
						raise FileNotFoundError('Файл для импорта не найден!')
				else:
					raise TypeError('Указан неверный тип! Должна быть строка!')
			
			#case 'ИМПОРТ-БЛ':
			#	if args[0]["type"] == 'типСТРОКА':
			#		try:
			#			with open(args[0]['raw'], 'r') as f:
			#				data = f.read()
			#			data = data.split('\n')
			#			tree_code += data			#TODO: тут надо много думать, не на сонную голову
			#		except FileNotFoundError:
			#			raise FileNotFoundError('Файл для импорта не найден!')
			#	else:
			#		raise TypeError('Указан неверный тип! Должна быть строка!')
			
			case 'НЕ':
				if args[0]["type"] == 'типПЕРЕМЕННАЯ':
					result.append(f'{args[0]["raw"]} = !{args[0]["raw"]};')
				else:
					raise TypeError('Указан неверный тип! Должно быть NOT по отношению к булево!')
			
			case 'ПРОДОЛЖИТЬ':
				result.append('continue;')
			
			case 'ПРЕРВАТЬ':
				result.append('break;')
			
			case 'СЛУЧАЙНО':
				if args[0]["type"] == 'типПЕРЕМЕННАЯ':
					result.append(f'int {args[0]["raw"]} = rand();')
				else:
					raise TypeError('Указан неверный тип! Должна быть переменная!')
		
	result = '\n\t'.join(result)
	result = DEFAULT.replace('<|BL-USERCODE|>', result)
	
	temp_file_name = f'tmp_BL{str(hash(result))[1:6]}.c' # Запись .c файла
	with open(temp_file_name, 'w', encoding='utf-8') as f:
		f.write(result)
	
	return_code = system('gcc '+flags+temp_file_name)
	
	if not settings['C-code']:
		remove(temp_file_name)
	
	return return_code
