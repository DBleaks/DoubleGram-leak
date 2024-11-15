#!/bin/env python3
# Author : Doublegram.com
import os, sys, requests, configparser, uuid, socket

global is_update
global last_version
global notice
global translations

translations = {}

lang = False

try:
	with open('data/lang.data', encoding="UTF-8") as f:
		cpass = configparser.RawConfigParser()
		cpass.read_file(f)

		for each_section in cpass.sections():
			for (each_key, each_val) in cpass.items(each_section):
				value = each_val

		lang = value

except IOError:
	print()
	print(" [+] Select your language")
	print(" 1 | English")
	print(" 2 | Italiano")
	print()

	choise = False

	while choise != '1' and choise != '2':
		choise = input("[+] -->")

	if choise == '1':
		chosen_lang = 'EN'
	elif choise == '2':
		chosen_lang = 'IT'
	else:
		chosen_lang = 'EN'
	
	lang_setting = configparser.RawConfigParser()
	lang_setting.add_section('lang')
	lang_setting.set('lang', 'choise', chosen_lang)
	setup = open('data/lang.data', 'w', encoding="UTF-8")
	lang_setting.write(setup)
	setup.close()

	lang = chosen_lang
	os.system('cls' if os.name=='nt' else 'clear')


if lang == 'IT' or lang == 'EN':
	with open('translations/'+lang+'.data', encoding="UTF-8") as f:
		cpass = configparser.RawConfigParser()
		cpass.read_file(f)

		for each_section in cpass.sections():
			for (each_key, each_val) in cpass.items(each_section):
				translations[each_key] = each_val

breaker = False 

current_version = '1.6.0'
current_edition = 'PRO_EDITION'
serial_id = 'EO9K2W3E9JRFMESORUBALI'

url = "https://run.doublegram.com/version_verification.php?edition="+current_edition

try:
	resp = requests.get(url)
	last_version = resp.text
except:
	print(" "+translations['impossibile_conn'])
	choise = input(" "+translations['invio_continuare'])
	breaker = False
	sys.exit()

url = "https://run.doublegram.com/notice.php?ver="+current_version+'&edition='+current_edition
resp = requests.get(url)
notice = resp.text	

if last_version != current_version and last_version != 'no':
	is_update = True
else:
	is_update = False

if notice == 'no':
	notice = False

cpass = configparser.RawConfigParser()

is_validated = True

if is_update == False:
	try:
		with open('data/license.data', encoding="UTF-8") as f:
			cpass.read_file(f)
			user = {}
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					user[each_key] = each_val

			dvc = socket.gethostname()

			if dvc == user['dvc_name'] and current_edition == user['edition']:
				url = "https://run.doublegram.com/verify.php?edition="+user['edition']+"&version="+user['version']+"&serial_id="+user['serial_id']+"&uid="+user['uid']+"&dvc_name="+user['dvc_name']+"&pcode="+user['pcode']
				resp = requests.get(url)
				is_user = resp.text

				if is_user == 'ok':
					is_validated = True
			else:
				print(translations['impossibile_verificare_licenza'])
				print(translations['problema_persiste'])
				choise = input(translations['invio_continuare'])

	except IOError:

		uid = uuid.uuid1()
		dvc = socket.gethostname()

		print(translations['inserisci_codice_acquisto'])
		choise = input("[+] -->")

		url = "https://run.doublegram.com/activate.php?key="+choise+'&edition='+current_edition+'&version='+current_version+"&serial_id="+serial_id+"&uid="+str(uid)+"&dvc_name="+dvc
		resp = requests.get(url)
		key_is_valid = resp.text

		if key_is_valid == 'ok':
			license = configparser.RawConfigParser()
			license.add_section('license_verification')
			license.set('license_verification', 'edition', current_edition)
			license.set('license_verification', 'version', current_version)
			license.set('license_verification', 'serial_ID', serial_id)
			license.set('license_verification', 'uid', uid)
			license.set('license_verification', 'dvc_name', dvc)
			license.set('license_verification', 'pcode', choise)
			setup = open('data/license.data', 'w', encoding="UTF-8")
			license.write(setup)
			setup.close()

			choise = input(translations['prodotto_validato'])

			is_validated = True

		elif key_is_valid == 'update':
			print(translations['impossibile_verificare_licenza'])
			print(translations['problema_persiste'])
			choise = input(translations['invio_continuare'])

		else:
			choise = input(translations['validazione_fallita'])
			breaker = False
else:
	try:
		with open('data/license.data', encoding="UTF-8") as f:
			cpass.read_file(f)
			user = {}
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					user[each_key] = each_val

			dvc = socket.gethostname()
			if dvc == user['dvc_name']:
				url = "https://run.doublegram.com/verify.php?edition="+user['edition']+"&version="+user['version']+"&serial_id="+user['serial_id']+"&uid="+user['uid']+"&dvc_name="+user['dvc_name']+"&pcode="+user['pcode']
				resp = requests.get(url)
				is_user = resp.text

				if is_user == 'ok':
					is_validated = True
				else:
					print(translations['impossibile_verificare_licenza'])
					print(translations['problema_persiste'])
					choise = input(translations['invio_continuare'])
					breaker = False

	except:
		print(translations['nuova_versione'])
		choise = input(translations['invio_continuare'])
		breaker = False

if breaker == False and is_validated == True:

	import banner, menu, settings

	if is_validated == True:
		settings.checkSettings(if_false_create=True)
		banner.banner(is_update,last_version,notice,start=True)
		menu.PrincipalMenu(show_menu=False)
	else:
		print(translations['impossibile_verificare_licenza'])
		print(translations['problema_persiste'])
		choise = input(translations['invio_continuare'])
