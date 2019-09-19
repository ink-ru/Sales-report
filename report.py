#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Выполнить код онлайн - https://rextester.com/CIIWO51060
Решение задачи с помощью SQL - # https://www.sql.ru/forum/1159023-2/konverter-nedel-v-mesyac-na-sql
'''

from __future__ import division

import os, sys, re, argparse
import datetime, time
import locale

try:
	import numpy as np
	#import pandas
except ImportError:
	print("You have to install numpy module before running this program!")
	print("Use - sudo pip3 install numpy")
	sys.exit(os.EX_UNAVAILABLE)

try:
	import pprint 
	print_mode = 'pprint'
except ImportError:
	print("pprint module havn't been found.")

'''
TODO: Перенести функции в подключаемый модуль
'''
'''
TODO: Перенести входные данные в файл или БД
'''
'''
TODO: Расширить календарь numpy праздничными днями - http://data.gov.ru/opendata/7708660670-proizvcalendar
'''

VERSION = "1.0.0"
DEBUG = False

'''
TODO: вынести вывод DEBUG и проверку его необходимотси в отдельную функцию
'''

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def createParser (): # http://jenyay.net/Programming/Argparse
	parser = argparse.ArgumentParser(
				prog = sys.argv[0],
				description = '''Convert weekly sales to months report''',
				epilog = '''george.a.wise@gmail.com'''
				)
	parser.add_argument ('-m', '-month', required=False, default='0', help = 'Номер месяца')
 
	return parser

def show_month(mnum='all'):
	if date == 'all':
		'''
		for (key, value) in data_per_month.items():
			print(key , ": ", value )
		'''
		pass
	elif date == 'current':
		# date = datetime.datetime.now()
		pass
	else:
		parser.print_help()
		sys.exit('Ошибка. Неправильный номер месяца') # raise ValueError('Ошибка. Неправильный адрес репозитория')
		return False

def convert_amount(data_dict):

	data_per_month = {}

	for key, value in data_dict.items():

		# Преведение формата дат
		start = datetime.datetime.strptime(key, "%d.%m.%Y") - datetime.timedelta(days=6)
		start_month = (datetime.datetime.strptime(key, "%d.%m.%Y") - datetime.timedelta(days=6)).month
		end = datetime.datetime.strptime(key, "%d.%m.%Y")
		end_month = datetime.datetime.strptime(key, "%d.%m.%Y").month

		value = float(value)

		if start_month != end_month:

			# Разбиваем интервал на два по месяцам
			start_2 = end.date().replace(day=1)
			end_2 = end.date()
			
			start_1 = start.date()
			end_1 = start_2 - datetime.timedelta (days = 1) # last_day_of_month

			# Определяем количество рабочих дней в интервалах
			# TODO: вынести в функцию
			busdays2 = np.busday_count( start_2, (end_2+datetime.timedelta (days = 1)))
			busdays1 = np.busday_count( start_1, (end_1+datetime.timedelta (days = 1)))

			busdays = busdays1+busdays2

			# Определяем объем продаж для каждого интервала
			amount1 = float(value)/busdays*busdays1
			amount2 = float(value)/busdays*busdays2

			if DEBUG:
				print( 'Месяца не совпадают: '+str(start_month)+" - "+str(end_month) )
			
				print( str(start_1)+" - "+str(end_1) +"("+str(busdays1)+")" )
				print( str(start_2)+" - "+str(end_2) +"("+str(busdays2)+")" )

			# переменные для использования в update
			key1 = str(start_1.month)
			key2 = str(end_2.month)

			# BUG: data_per_month[str(start_1.month)] += amount1
			if key1 in data_per_month:
				# data_per_month.update(key1 = amount1)
				data_per_month[key1] = data_per_month[key1]+amount1
			else:
				data_per_month[key1] = amount1

			# BUG: data_per_month[str(end_2.month)] += amount2
			if key2 in data_per_month:
				# data_per_month.update(key2 = amount2)
				data_per_month[key2] = data_per_month[key2] + amount2
			else:
				data_per_month[key2] = amount2

			if DEBUG:
				print( str(amount1) + " + " + str(amount2) + " = " + str(value))
		else:
			if DEBUG:
				print(str(start.date()))
				print(str(end.date()))

			key1 = str(end.date().month)

			# data_per_month[str(end.date().month)] += value
			if key1 in data_per_month:
				#data_per_month.update(key1 = value)
				data_per_month[key1] = data_per_month[key1]+value
			else:
				data_per_month[key1] = value

		if DEBUG:
			print("Amount: "+str(value))
			print('-------')
	return data_per_month

def main(argv):

	parser = createParser()
	namespace = parser.parse_args()

	month_number = str(namespace.m).strip().rstrip('0') # sys.argv[1]

	if 'TERM' in os.environ: #os.environ['TERM']:
		if sys.platform == 'win32' or os.name=='nt':
			locale.setlocale(locale.LC_ALL, 'rus_rus')
		else:
			locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
		rows, columns = os.popen('stty size', 'r').read().split()
		cls()
	else:
		columns = 40

	data_dict = {
	"26.02.2013": "312.00",
	"05.03.2013": "833.00",
	"12.03.2013": "225.00",
	"19.03.2013": "453.00",
	"26.03.2013": "774.00",
	"02.04.2013": "719.00",
	"09.04.2013": "136.00",
	"16.04.2013": "133.00",
	"23.04.2013": "157.00",
	"30.04.2013": "850.00",
	"07.05.2013": "940.00",
	"14.05.2013": "933.00",
	"21.05.2013": "422.00",
	"28.05.2013": "952.00",
	"04.06.2013": "136.00",
	"11.06.2013": "701.00"
	}

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	print ('▓'*int(columns))

	# ═════════════════════════════════════════════════════════════════════════
	print ('═'*int(columns))

	pprint.pprint(data_dict, indent=2, depth=1, width=60, compact=True)

	q = '\nВ таблице хранятся сведения о еженедельных продажах продукта. Необходимо настроить автоматическое преобразование еженедельных значений в ежемесячные. Продажи в переходных неделях (часть недели в одном месяце, часть в другом) необходимо распределить по будним дням (исключая выходные дни - сб, вск).\n'
	print(q)

	# ═════════════════════════════════════════════════════════════════════════
	print ('═'*int(columns))

	data_per_month = convert_amount(data_dict)

	# elif month_number == 'all':
	# 	print("Данные по месяцам: ")
	# 	pprint.pprint(data_per_month, indent=2, depth=1, width=60, compact=True)
	if len(month_number) > 0 and int(month_number) in range(1,31):
		print("Данные за месяц ("+month_number+"): ")
		if month_number in data_per_month:
			pprint.pprint(data_per_month[month_number], indent=2, depth=1, width=60, compact=True)
		else:
			print("нет данных")
	else:
		print("Данные по месяцам: ")
		pprint.pprint(data_per_month, indent=2, depth=1, width=60, compact=True)
		'''
		parser.print_help()
		# raise ValueError('Ошибка. Неправильный номер месяца')
		sys.exit(os.EX_USAGE)
		'''

	print()

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	print ('▓'*int(columns))

	sys.exit(os.EX_OK) # code 0, all ok

if __name__ == '__main__':
	# main(argv)
	main(sys.argv)
else:
	sys.exit(os.EX_USAGE) # https://docs.python.org/2/library/os.html
