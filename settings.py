import os, configparser, colors, banner, menu, re, sys, csv
import configparser
import pandas as pd

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
	print(" [+] Choose a language")
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

	lang = choise

if lang == 'IT' or lang == 'EN':
	with open('translations/'+lang+'.data', encoding="UTF-8") as f:
		cpass = configparser.RawConfigParser()
		cpass.read_file(f)

		for each_section in cpass.sections():
			for (each_key, each_val) in cpass.items(each_section):
				translations[each_key] = each_val


colors.getColors()


def checkSettings(if_false_create):
	cpass = configparser.RawConfigParser()
	try:
		with open('data/settings.data', encoding="UTF-8") as f:
			cpass.read_file(f)

			# Check if in the adding_settings section there is the "premium_filter" setting, if not add it
			found = False
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					if each_section == 'adding_settings' and each_key == 'premium_filter':
						found = True
			
			if found == False:
				settings = configparser.RawConfigParser()
				settings.read('data/settings.data', encoding='UTF-8')
				# The adding_settings section is already present, add the missing setting only
				settings.set("adding_settings", "premium_filter", translations['both_premium'])
				setup = open("data/settings.data", "w", encoding="utf-8")
				settings.write(setup)
				setup.close()

			# Check if there is a section called "scraping_settings" in settings.data, if not add it
			found = False
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					if each_section == 'scraping_settings':
						found = True
			
			if found == False:
				settings = configparser.RawConfigParser()
				settings.read('data/settings.data', encoding='UTF-8')
				settings.add_section("scraping_settings")
				settings.set("scraping_settings", "deep_search_vowels", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_consonants_1", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_consonants_2", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_accented", translations['abilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_symbols_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_symbols_2", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_numbers", translations['abilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_emoji_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_emoji_2", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_russian_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_russian_2", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_russian_3", translations['disabilitato_first_cap'])
			
				settings.set("scraping_settings", "stop_deep_search_percentage", "50")
				settings.set("scraping_settings", "stop_deep_search_percentage_status", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_pause", "0.50 "+translations['abbreviazione_secondi'])

				setup = open("data/settings.data", "w", encoding="utf-8")
				settings.write(setup)
				setup.close()

			found = False
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					if each_section == 'scraping_settings' and each_key == 'blacklist_status':
						found = True
			
			if found == False:
				settings = configparser.RawConfigParser()
				settings.read('data/settings.data', encoding='UTF-8')
				settings.set("scraping_settings", "blacklist_status", translations['disabilitato_first_cap'])
				setup = open("data/settings.data", "w", encoding="utf-8")
				settings.write(setup)
				setup.close()

			
						
			return True
		
	except IOError:
		print(colors.wy+" "+translations['impostazioni_base_configurate'])
		if if_false_create == False:
			return False
		else:
			print("creating settings")
			log = False
			settings = configparser.RawConfigParser()
			settings.add_section("general_settings")
			settings.set("general_settings", "log", translations['disabilitato_first_cap'])
			settings.set("general_settings", "analyze_account", "/")
			settings.set("general_settings", "between_autoinvite_pause", "1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("general_settings", "between_invite_pause", "1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")

			setup = open("data/settings.data", "w", encoding="utf-8")
			settings.write(setup)


			settings.add_section("adding_settings")
			settings.set("adding_settings", "between_autoinvite_pause", "1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "auto_add_at_start", translations['disabilitato_first_cap'])
			settings.set("adding_settings", "if_account_out", translations['abilitato_first_cap'])
			settings.set("adding_settings", "change_account_n_requests", "20 "+translations['richieste'])
			settings.set("adding_settings", "change_account_pause", "1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "consecutive_error_breaker", "30 "+translations['errori'])
			settings.set("adding_settings", "start_point_members_file", translations['da_interrotto'])
			settings.set("adding_settings", "add_using", translations['user_id_opt'])
			settings.set("adding_settings", "between_adding_pause", "1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "casual_pause_times", "3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "exclude_bot", translations['abilitato_first_cap'])
			settings.set("adding_settings", "exclude_admin", translations['abilitato_first_cap'])
			settings.set("adding_settings", "photo_forcing", translations['abilitato_first_cap'])
			settings.set("adding_settings", "filter_last_seen", translations['nessuna_restrizione'])
			settings.set("adding_settings", "filter_dc", translations['nessuna_restrizione'])
			settings.set("adding_settings", "filter_phone_number", translations['disabilitato_first_cap'])
			settings.set("adding_settings", "stop_max_adding", translations['nessun_limite'])
			settings.set("adding_settings", "continuous_adding", translations['disabilitato_first_cap'])
			settings.set("adding_settings", "ca_ripet", translations['infinito'])
			settings.set("adding_settings", "ca_pause", translations['nessuna_pausa'])
			settings.set("adding_settings", "premium_filter", translations['both_premium'])

			setup = open("data/settings.data", "w", encoding="utf-8")
			settings.write(setup)

			settings.add_section("scraping_settings")
			settings.set("scraping_settings", "deep_search_vowels", translations['abilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_consonants_1", translations['abilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_consonants_2", translations['disabilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_accented", translations['abilitato_first_cap'])

			settings.set("scraping_settings", "deep_search_symbols_1", translations['disabilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_symbols_2", translations['disabilitato_first_cap'])

			settings.set("scraping_settings", "deep_search_numbers", translations['abilitato_first_cap'])

			settings.set("scraping_settings", "deep_search_emoji_1", translations['disabilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_emoji_2", translations['disabilitato_first_cap'])

			settings.set("scraping_settings", "deep_search_russian_1", translations['disabilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_russian_2", translations['disabilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_russian_3", translations['disabilitato_first_cap'])
		
			settings.set("scraping_settings", "stop_deep_search_percentage", "50")
			settings.set("scraping_settings", "stop_deep_search_percentage_status", translations['abilitato_first_cap'])
			settings.set("scraping_settings", "deep_search_pause", "0.50 "+translations['abbreviazione_secondi'])

			setup = open("data/settings.data", "w", encoding="utf-8")
			settings.write(setup)
			
			setup.close()

			return log


def getSetting(name,section):
	cpass = configparser.RawConfigParser()
	cpass.read('data/settings.data', encoding='UTF-8')

	value = 'False'

	for each_section in cpass.sections():
		for (each_key, each_val) in cpass.items(each_section):
			if each_section == section and each_key == name:
				value = each_val

	if name == 'log' and value == 'False':
		value = translations['disabilitato_first_cap']
		
	return value


def getLang():
	cpass = configparser.RawConfigParser()
	cpass.read('data/lang.data', encoding='UTF-8')

	value = 'False'

	for each_section in cpass.sections():
		for (each_key, each_val) in cpass.items(each_section):
			value = each_val

	if value == 'IT':
		value = 'Italiano'
	elif value == 'EN':
		value = 'English'

	return value


def SetLanguage():
	log = getSetting('log','general_settings')

	language = getLang()

	print()
	print(colors.wm+colors.wy+" "+translations['modifica_lingua_cap']+" "+colors.wreset)
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"English")
	print(colors.cy+"  2 | "+colors.wy+"Italiano")
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetLanguage()

	new_lang = 'EN'

	if int(choise) == 1:
		new_lang = 'EN'
	elif int(choise) == 2:
		new_lang = 'IT'

	config = configparser.ConfigParser()
	config.read('data/lang.data', encoding="UTF-8")  
	cnfFile = open('data/lang.data', "w", encoding="UTF-8")
	config.set("lang","choise",new_lang)
	config.write(cnfFile)
	cnfFile.close()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	os.remove("data/settings.data")

	if os.name=='nt':
		print()
		print(" [+] "+translations['riavvio_necessario'])
		print(" [+] "+translations['riavvio_necessario_1'])
		print(colors.wreset)
		sys.exit()
	else:
		python = sys.executable
		os.execl(python, python, * sys.argv)

	
def SetLogs():
	log = getSetting('log','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['mantieni_log_cap']+" "+colors.wreset)
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","log",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()
		log = translations['abilitato_first_cap']
		
		if os.name=='nt':
			print()
			print(" [+] "+translations['riavvio_necessario'])
			print(" [+] "+translations['riavvio_necessario_1'])
			print(colors.wreset)
			sys.exit()
		else:
			python = sys.executable
			os.execl(python, python, * sys.argv)

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","log",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()
		log = translations['disabilitato_first_cap']

		if os.name=='nt':
			print()
			print(" [+] "+translations['riavvio_necessario'])
			print(" [+] "+translations['riavvio_necessario_1'])
			print(colors.wreset)
			sys.exit()
		else:
			python = sys.executable
			os.execl(python, python, * sys.argv)

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetLogs()


def SetAnalyzeAccount():
	log = getSetting('log','general_settings')

	analyze_account = getSetting('analyze_account','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['account_analisi_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['account_analisi_cap_txt_1'])
	print(colors.wy+" "+translations['account_analisi_cap_txt_2'])
	print(colors.wy+" "+translations['account_analisi_cap_txt_3'])
	print(colors.wy+" "+translations['account_analisi_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['inserisci_username_manualmente'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")
		
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		choise = menu.setChoise()

		config.set("general_settings","analyze_account",choise)
		config.write(cnfFile)
		cnfFile.close()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetAnalyzeAccount()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	menu.SettingsMenu()


def SetBlacklistStatus():
	log = getSetting('log','general_settings')

	blacklist_status = getSetting('blacklist_status','scraping_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['blacklist_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['blacklist_cap_txt_1'])
	print(colors.wy+" "+translations['blacklist_cap_txt_2'])
	print(colors.wy+" "+translations['blacklist_cap_txt_3'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","blacklist_status",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.ScrapingSettings()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","blacklist_status",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.ScrapingSettings()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBlacklistStatus()

def AddUserToBlacklist():
	log = getSetting('log','general_settings')

	#User can enter a custom number
	print()
	print(colors.wm+colors.wy+" "+translations['aggiungi_utente_blacklist_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['insert_id_username'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	
	# Chiede all'utente di inserire un valore
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()

	valid = True
	# Check if the user has entered a number or a username (starts with @)
	if choise != '' and choise[0] == '@' and len(choise) > 3:
		pass

	else:
		try:
			# check if choise is a number with or without - at the beginning
			if choise[0] == '-':
				choise_test = choise[1:]
			else:
				choise_test = choise
			
			int(choise_test)

		except:
			valid = False
	
	if valid == False:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddUserToBlacklist()
	
	# Check if the blacklist.csv file exists, if not create it
	if not os.path.exists('members/blacklist.csv'):
		with open('members/blacklist.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["username_id"])
	
	# Check if the user is already in the blacklist.csv file
	found = False
	with open('members/blacklist.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			if choise in row:
				found = True
				print()
				print(colors.wy+" "+translations['utente_gia_blacklist'])
				print()
				AddUserToBlacklist()
		
	# Add the user to the blacklist.csv file
	if found == False:
		with open('members/blacklist.csv', 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([choise])

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()


def RemoveDuplicates():
	log = getSetting('log','general_settings')
	done = True
	try:
		# Carica il file CSV in un DataFrame
		df = pd.read_csv('members/members.csv')

		# Rimuove le righe duplicate in base all'ID utente
		df_cleaned = df.drop_duplicates(subset=['user id'])

		# Salva il DataFrame pulito in un nuovo file CSV
		df_cleaned.to_csv('members/members.csv', index=False)

	except Exception as e:
		done = False
		print(translations['errore_rimuovi_duplicati'])
	
	if done == True:
		print()
		print(colors.wy+" "+translations['rimuovi_duplicati_fatto'])
		print()
	
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ScrapingSettings()


def RemoveUserFromBlacklist():
	log = getSetting('log','general_settings')

	if not os.path.exists('members/blacklist.csv'):
		print()
		print(colors.re+" [!] "+translations['blacklist_non_trovata']+colors.wreset)
		print()
		choise = input(" "+translations['invio_continuare'])
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	# Check if the blacklist.csv file is empty
	if os.stat('members/blacklist.csv').st_size == 1:
		print()
		print(colors.re+" "+translations['blacklist_vuota']+colors.wreset)
		print()
		menu.ScrapingSettings()


	# Read the blacklist.csv file
	blacklist = []
	with open('members/blacklist.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				blacklist.append(row[0])
			except:
				pass
	
	if len(blacklist) == 1:
		print()
		print(colors.re+" "+translations['blacklist_vuota']+colors.wreset)
		print()
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	# Print the blacklist.csv file
	print()
	print(colors.wm+colors.wy+" "+translations['rimuovi_utente_blacklist_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['rimuovi_utente_blacklist_cap_txt_1'])
	print()


	for i in range(len(blacklist)):
		if i != 0:
			print(" "+str(i)+" | "+blacklist[i])
	
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	
	# Ask the user to choose a user to remove from the blacklist.csv file
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		RemoveUserFromBlacklist()
	
	# Check if the user has entered a valid number
	if int(choise) < 1 or int(choise) >= len(blacklist):
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		RemoveUserFromBlacklist()
	
	# Delete the user from the blacklist.csv file
	with open('members/blacklist.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		for i in range(len(blacklist)):
			if i != int(choise):
				writer.writerow([blacklist[i]])

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	RemoveUserFromBlacklist()



def RemoveBlacklistedUsers():
	log = getSetting('log','general_settings')

	if not os.path.exists('members/blacklist.csv'):
		print()
		print(colors.re+" [!] "+translations['blacklist_non_trovata']+colors.wreset)
		print()
		choise = input(" "+translations['invio_continuare'])
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	# Check if the blacklist.csv file is empty
	if os.stat('members/blacklist.csv').st_size == 1:
		print()
		print(colors.wy+" "+translations['blacklist_vuota'])
		print()
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
		
	
	# Read the blacklist.csv file
	blacklist = []
	with open('members/blacklist.csv', 'r', encoding="utf-8") as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				blacklist.append(row[0])
			except:
				pass
	
	if len(blacklist) == 1:
		print()
		print(colors.re+" "+translations['blacklist_vuota']+colors.wreset)
		print()
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	# Check if the members.csv file exists
	if not os.path.exists('members/members.csv'):
		print(colors.re+" [!] "+translations['lista_non_trovata'])
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()

	# Read the members.csv file
	members = []
	members_id = []
	members_usernames = []
	with open('members/members.csv', 'r', encoding="utf-8") as file:
		reader = csv.reader(file)
		for row in reader:
			#if not empty row[1]
			if row[1] != '':
				members_id.append(row[1])
			else:
				members_id.append(False)
			
			#if not empty row[0]
			if row[0] != '':
				members_usernames.append(row[0])
			else:
				members_usernames.append(False)
			
			
			members.append(row)

	# Check if the members.csv file is empty
	if len(members) == 0:
		print()
		print(colors.wy+" "+translations['lista_vuota'])
		print()
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	# Create an array with the members that are not in the blacklist.csv file
	members_cleaned = []
	for i in range(len(members)):
		if members_id[i] not in blacklist and members_usernames[i] not in blacklist:
			members_cleaned.append(members[i])
	
	# Recreate the members.csv file with the cleaned array
	with open("members/members.csv","w",encoding='UTF-8') as f:
		writer = csv.writer(f,delimiter=",",lineterminator="\n")

		# Compone la riga con i dati per ogni utente di members_cleaned e scrive la riga nel file
		for i in range(len(members_cleaned)):
			writer.writerow(members_cleaned[i])
		
	f.close()


	print()
	print(colors.wy+" "+translations['utenti_blacklist_rimossi'])
	print()

	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ScrapingSettings()
	


def SetAutoInvite():
	log = getSetting('log','general_settings')

	auto_add_at_start = getSetting('auto_add_at_start','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['invito_automatico_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['invito_automatico_cap_txt_1'])
	print(colors.wy+" "+translations['invito_automatico_cap_txt_2'])
	print(colors.wy+" "+translations['invito_automatico_cap_txt_3'])
	print(colors.wy+" "+translations['invito_automatico_cap_txt_4'])
	print(colors.wy+" "+translations['invito_automatico_cap_txt_5'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","auto_add_at_start",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","auto_add_at_start",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetAutoInvite()

def SetDeepSearchCharacters():
	log = getSetting('log','general_settings')

	# CHeck if deep_search_characters is in settings.data
	try:
		with open('data/settings.data', encoding="UTF-8") as f:
			cpass = configparser.RawConfigParser()
			cpass.read_file(f)

			found = False

			# check if scraping_settings section is in settings.data
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					if each_section == 'scraping_settings':
						found = True
			
			if found == False:
				settings = configparser.RawConfigParser()
				settings.add_section("scraping_settings")
				settings.set("scraping_settings", "deep_search_vowels", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_consonants_1", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_consonants_2", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_accented", translations['abilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_symbols_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_symbols_2", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_numbers", translations['abilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_emoji_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_emoji_2", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_russian_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_russian_2", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_russian_3", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "stop_deep_search_percentage", "50")
				settings.set("scraping_settings", "stop_deep_search_percentage_status", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_pause", "0.50 "+translations['abbreviazione_secondi'])

				setup = open("data/settings.data", "a", encoding="utf-8")
				settings.write(setup)
				setup.close()
	
	except IOError:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		checkSettings(True)
		print(colors.wy+" "+translations['impostazioni_base_configurate'])
		SetDeepSearchCharacters()

	risk = 0

	deep_search_vowels = getSetting('deep_search_vowels','scraping_settings')
	deep_search_consonant_1 = getSetting('deep_search_consonant_1','scraping_settings')
	deep_search_consonant_2 = getSetting('deep_search_consonant_2','scraping_settings')
	deep_search_accented = getSetting('deep_search_accented','scraping_settings')
	deep_search_symbols_1 = getSetting('deep_search_symbols_1','scraping_settings')
	deep_search_symbols_2 = getSetting('deep_search_symbols_2','scraping_settings')
	deep_search_numbers = getSetting('deep_search_numbers','scraping_settings')
	deep_search_emoji_1 = getSetting('deep_search_emoji_1','scraping_settings')
	deep_search_emoji_2 = getSetting('deep_search_emoji_2','scraping_settings')
	deep_search_russian_1 = getSetting('deep_search_russian_1','scraping_settings')
	deep_search_russian_2 = getSetting('deep_search_russian_2','scraping_settings')
	deep_search_russian_3 = getSetting('deep_search_russian_3','scraping_settings')


	# Set
	vowels = 6
	consontant_1 = 10
	consontant_2 = 10
	
	accented = 6
	
	symbols_1 = 13
	symbols_2 = 15

	numbers = 10
	
	#most used emoji for usernames
	emoji_1 = 10
	emoji_2 = 7

	russian_1 = 10
	russian_2 = 10
	russian_3 = 10 

	# calculate the total risk. Each setting is worth the length of the set
	if deep_search_vowels == translations['abilitato_first_cap']:
		risk += vowels
	if deep_search_consonant_1 == translations['abilitato_first_cap']:
		risk += consontant_1
	if deep_search_consonant_2 == translations['abilitato_first_cap']:
		risk += consontant_2
	if deep_search_accented == translations['abilitato_first_cap']:
		risk += accented
	if deep_search_symbols_1 == translations['abilitato_first_cap']:
		risk += symbols_1
	if deep_search_symbols_2 == translations['abilitato_first_cap']:
		risk += symbols_2
	if deep_search_numbers == translations['abilitato_first_cap']:
		risk += numbers
	if deep_search_emoji_1 == translations['abilitato_first_cap']:
		risk += emoji_1
	if deep_search_emoji_2 == translations['abilitato_first_cap']:
		risk += emoji_2
	if deep_search_russian_1 == translations['abilitato_first_cap']:
		risk += russian_1
	if deep_search_russian_2 == translations['abilitato_first_cap']:
		risk += russian_2
	if deep_search_russian_3 == translations['abilitato_first_cap']:
		risk += russian_3


	risk = int((risk * 100) / 117)
	
	
	# Enable / Disable menu for each setting

	print()
	print(colors.wm+colors.wy+" "+translations['enable_disable_charset_cap']+" "+colors.wreset)
	print()
	print(colors.gr+" "+translations['select_a_charset']+" ")
	print()
	print(colors.cy+translations['ab_dis_line'])
	print("      "+colors.wg+colors.wy+'  '+colors.wreset+ " = "+translations['abilitato_cap']+"    "+colors.wr+colors.wy+'  '+colors.wreset+ " = "+translations['dis_cap'])
	print(colors.cy+translations['ab_dis_line'])

	if deep_search_vowels == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset
	
	print(colors.cy+"  1 | "+status+translations['vocali'])

	if deep_search_consonant_1 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  2 | "+status+translations['consonanti_1'])

	if deep_search_consonant_2 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  3 | "+status+translations['consonanti_2'])

	if deep_search_accented == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  4 | "+status+translations['accentate'])

	if deep_search_symbols_1 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  5 | "+status+translations['simboli_1'])

	if deep_search_symbols_2 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  6 | "+status+translations['simboli_2'])

	if deep_search_numbers == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  7 | "+status+translations['numeri'])

	if deep_search_emoji_1 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  8 | "+status+translations['emoji_1'])

	if deep_search_emoji_2 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+"  9 | "+status+translations['emoji_2'])

	if deep_search_russian_1 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+" 10 | "+status+translations['russian_1'])

	if deep_search_russian_2 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+" 11 | "+status+translations['russian_2'])

	if deep_search_russian_3 == translations['abilitato_first_cap']:
		status = colors.wg+colors.wy+'  '+colors.wreset
	else:
		status = colors.wr+colors.wy+'  '+colors.wreset

	print(colors.cy+" 12 | "+status+translations['russian_3'])

	print()
	print(" - Your exstimated risk level is: "+str(risk)+"/100")

	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	elif choise == '1':
		if deep_search_vowels == translations['abilitato_first_cap']:
			deep_search_vowels = 'Disabled'
		else:
			deep_search_vowels = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_vowels",deep_search_vowels)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '2':
		if deep_search_consonant_1 == translations['abilitato_first_cap']:
			deep_search_consonant_1 = translations['disabilitato_first_cap']
		else:
			deep_search_consonant_1 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_consonant_1",deep_search_consonant_1)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '3':
		if deep_search_consonant_2 == translations['abilitato_first_cap']:
			deep_search_consonant_2 = translations['disabilitato_first_cap']
		else:
			deep_search_consonant_2 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_consonant_2",deep_search_consonant_2)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '4':
		if deep_search_accented == translations['abilitato_first_cap']:
			deep_search_accented = translations['disabilitato_first_cap']
		else:
			deep_search_accented = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_accented",deep_search_accented)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '5':
		if deep_search_symbols_1 == translations['abilitato_first_cap']:
			deep_search_symbols_1 = translations['disabilitato_first_cap']
		else:
			deep_search_symbols_1 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_symbols_1",deep_search_symbols_1)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '6':
		if deep_search_symbols_2 == translations['abilitato_first_cap']:
			deep_search_symbols_2 = translations['disabilitato_first_cap']
		else:
			deep_search_symbols_2 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_symbols_2",deep_search_symbols_2)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '7':
		if deep_search_numbers == translations['abilitato_first_cap']:
			deep_search_numbers = translations['disabilitato_first_cap']
		else:
			deep_search_numbers = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_numbers",deep_search_numbers)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '8':
		if deep_search_emoji_1 == translations['abilitato_first_cap']:
			deep_search_emoji_1 = translations['disabilitato_first_cap']
		else:
			deep_search_emoji_1 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_emoji_1",deep_search_emoji_1)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '9':
		if deep_search_emoji_2 == translations['abilitato_first_cap']:
			deep_search_emoji_2 = translations['disabilitato_first_cap']
		else:
			deep_search_emoji_2 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_emoji_2",deep_search_emoji_2)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '10':
		if deep_search_russian_1 == translations['abilitato_first_cap']:
			deep_search_russian_1 = translations['disabilitato_first_cap']
		else:
			deep_search_russian_1 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_russian_1",deep_search_russian_1)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '11':
		if deep_search_russian_2 == translations['abilitato_first_cap']:
			deep_search_russian_2 = translations['disabilitato_first_cap']
		else:
			deep_search_russian_2 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_russian_2",deep_search_russian_2)
		config.write(cnfFile)
		cnfFile.close()
	
	elif choise == '12':
		if deep_search_russian_3 == translations['abilitato_first_cap']:
			deep_search_russian_3 = translations['disabilitato_first_cap']
		else:
			deep_search_russian_3 = translations['abilitato_first_cap']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_russian_3",deep_search_russian_3)
		config.write(cnfFile)
		cnfFile.close()

	
	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetDeepSearchCharacters()

	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	SetDeepSearchCharacters()

def SetStopScrapingUntilReached():
	log = getSetting('log','general_settings')

	stop_deep_search_percentage = getSetting('stop_deep_search_percentage','scraping_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['ferma_scraping_fino_a_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_txt_1'])
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_txt_2'])
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_txt_3'])
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_txt_4'])
	
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['imposta_percentuale'])
	print()

	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()
	
	elif choise == '1':
		
		# while che chiede all'utente un numero o una q
		while True:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			#User can enter a custom number
			print()
			print(colors.wm+colors.wy+" "+translations['ferma_scraping_fino_a_cap']+" "+colors.wreset)
			print()
			print(colors.wy+" "+translations['imposta_ferma_scraping_fino_a_cap_txt_1'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
			print()

			choise = menu.setChoise()

			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				menu.ScrapingSettings()
			try:
				int(choise)
				if int(choise) >= 0 and int(choise) <= 100:
					break
			except:
				pass

		if choise == 'q' or choise == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.ScrapingSettings()
		
		
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","stop_deep_search_percentage",choise)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.ScrapingSettings()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetStopScrapingUntilReached()


def SetStopScrapingUntilReachedStatus():
	log = getSetting('log','general_settings')

	stop_deep_search_percentage_status = getSetting('stop_deep_search_percentage_status','scraping_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['ferma_scraping_fino_a_status_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_status_txt_1'])
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_status_txt_2'])
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_status_txt_3'])
	print(colors.wy+" "+translations['ferma_scraping_fino_a_cap_status_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","stop_deep_search_percentage_status",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.ScrapingSettings()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","stop_deep_search_percentage_status",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()
	
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		
		menu.ScrapingSettings()
	
	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetStopScrapingUntilReachedStatus()
	
	

def SetPauseBetweenScrapingRequests():
	log = getSetting('log','general_settings')

	# CHeck if deep_search_characters is in settings.data
	try:
		with open('data/settings.data', encoding="UTF-8") as f:
			cpass = configparser.RawConfigParser()
			cpass.read_file(f)

			found = False

			# check if scraping_settings section is in settings.data
			for each_section in cpass.sections():
				for (each_key, each_val) in cpass.items(each_section):
					if each_section == 'scraping_settings':
						found = True
			
			if found == False:
				settings = configparser.RawConfigParser()
				settings.add_section("scraping_settings")

				settings.set("scraping_settings", "deep_search_vowels", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_consonants_1", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_consonants_2", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_accented", translations['abilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_symbols_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_symbols_2", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_numbers", translations['abilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_emoji_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_emoji_2", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "deep_search_russian_1", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_russian_2", translations['disabilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_russian_3", translations['disabilitato_first_cap'])

				settings.set("scraping_settings", "stop_deep_search_percentage", "50")
				settings.set("scraping_settings", "stop_deep_search_percentage_status", translations['abilitato_first_cap'])
				settings.set("scraping_settings", "deep_search_pause", "0.50 "+translations['abbreviazione_secondi'])

				setup = open("data/settings.data", "a", encoding="utf-8")
				settings.write(setup)
				setup.close()
	
	except IOError:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		checkSettings(True)
		print(colors.wy+" "+translations['impostazioni_base_configurate'])
		SetDeepSearchCharacters()

	
	deep_search_pause = getSetting('deep_search_pause','scraping_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_tra_richieste_scraping_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_tra_richieste_scraping_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_tra_richieste_scraping_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_tra_richieste_scraping_cap_txt_3'])
	print(colors.wy+" "+translations['pausa_tra_richieste_scraping_cap_txt_4'])
	
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['imposta_pausa'])
	print()

	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ScrapingSettings()

	elif choise == '1':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		#User can enter a custom number
		print()
		print(colors.wm+colors.wy+" "+translations['pausa_tra_richieste_scraping_cap']+" "+colors.wreset)
		print()
		print(colors.wy+" "+translations['imposta_pausa_tra_richieste_scraping_cap_txt_1'])
		print()
		print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
		print()
		
		# Chiede all'utente di inserire un numero
		while True:
			choise = menu.setChoise()

			if choise == 'q' or choise == 'Q' or  re.match("^[0-9]+(\.[0-9]{1,2})?$", choise):
				break

		# Check if the input is between 0.50 and 7200
		if re.match("^[0-9]+(\.[0-9]{1,2})?$", choise):
			choise = float(choise)
			if choise >= 0.50 and choise <= 86400:
				choise = str(choise)+" "+translations['abbreviazione_secondi']
			else:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				SetPauseBetweenScrapingRequests()
		
		else:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			SetPauseBetweenScrapingRequests()

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("scraping_settings","deep_search_pause",choise)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.ScrapingSettings()
	
	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetPauseBetweenScrapingRequests()


def SetPremiumFilter():
	log = getSetting('log','general_settings')

	premium_filter = getSetting('premium_filter','adding_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['filtro_premium_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['filtro_premium_cap_txt_1'])
	print(colors.wy+" "+translations['filtro_premium_cap_txt_2'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['only_premium'])
	print(colors.cy+" 2 | "+colors.wy+translations['only_non_premium'])
	print(colors.cy+" 3 | "+colors.wy+translations['both_premium'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()
	
	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","premium_filter",translations['only_premium'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()
	
	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","premium_filter",translations['only_non_premium'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '3':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","premium_filter",translations['both_premium'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()
	
	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetPremiumFilter()



def SetContinuousAdding():
	log = getSetting('log','general_settings')

	continuous_adding = getSetting('continuous_adding','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['abilita_ca_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['abilita_ca_cap_txt_1'])
	print(colors.wy+" "+translations['abilita_ca_cap_txt_2'])
	print(colors.wy+" "+translations['abilita_ca_cap_txt_3'])
	print(colors.wy+" "+translations['abilita_ca_cap_txt_4'])
	print(colors.wy+" "+translations['abilita_ca_cap_txt_5'])
	print(colors.wy+" "+translations['abilita_ca_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","continuous_adding",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","continuous_adding",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetContinuousAdding()


def SetContinuousAddingRipet():
	log = getSetting('log','general_settings')

	ca_ripet = getSetting('ca_ripet','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['cicli_ca_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['cicli_ca_cap_txt_1'])
	print(colors.wy+" "+translations['cicli_ca_cap_txt_2'])
	print(colors.wy+" "+translations['cicli_ca_cap_txt_3'])
	print(colors.wy+" "+translations['cicli_ca_cap_txt_4'])
	print(colors.wy+" "+translations['cicli_ca_cap_txt_5'])
	print(colors.wy+" "+translations['cicli_ca_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"2 "+translations['cicli'])
	print(colors.cy+"  2 | "+colors.wy+"3 "+translations['cicli'])
	print(colors.cy+"  3 | "+colors.wy+"4 "+translations['cicli'])
	print(colors.cy+"  4 | "+colors.wy+"5 "+translations['cicli'])
	print(colors.cy+"  5 | "+colors.wy+"10 "+translations['cicli'])
	print(colors.cy+"  6 | "+colors.wy+"15 "+translations['cicli'])
	print(colors.cy+"  7 | "+colors.wy+"20 "+translations['cicli'])
	print(colors.cy+"  8 | "+colors.wy+"25 "+translations['cicli'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['cicli'])
	print(colors.cy+" 10 | "+colors.wy+"35 "+translations['cicli'])
	print(colors.cy+" 11 | "+colors.wy+"40 "+translations['cicli'])
	print(colors.cy+" 12 | "+colors.wy+"45 "+translations['cicli'])
	print(colors.cy+" 13 | "+colors.wy+"50 "+translations['cicli'])
	print(colors.cy+" 14 | "+colors.wy+"75 "+translations['cicli'])
	print(colors.cy+" 15 | "+colors.wy+"100 "+translations['cicli'])
	print(colors.cy+" 16 | "+colors.wy+translations['infinito'])
	print(colors.cy+" 17 | "+colors.wy+translations['inserisci_valore_personalizzato'])


	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1' or choise == '2' or choise == '3' or choise == '4':
		ca_ripet = int(choise)+1
		ca_ripet = str(ca_ripet)+" "+translations['cicli']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_ripet",ca_ripet)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '5' or choise == '6' or choise == '7' or choise == '8' or choise == '9' or choise == '10' or choise == '11' or choise == '12' or choise == '13':
		if choise == '5':
			ca_ripet = '10 '+translations['cicli']
		elif choise == '6':
			ca_ripet = '15 '+translations['cicli']
		elif choise == '7':
			ca_ripet = '20 '+translations['cicli']
		elif choise == '8':
			ca_ripet = '25 '+translations['cicli']
		elif choise == '9':
			ca_ripet = '30 '+translations['cicli']
		elif choise == '10':
			ca_ripet = '35 '+translations['cicli']
		elif choise == '11':
			ca_ripet = '40 '+translations['cicli']
		elif choise == '12':
			ca_ripet = '45 '+translations['cicli']
		elif choise == '13':
			ca_ripet = '50 '+translations['cicli']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_ripet",ca_ripet)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '14':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_ripet",'75 '+translations['cicli'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '15':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_ripet",'100 '+translations['cicli'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '16':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_ripet",translations['infinito'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '17':
		while True:
			print()
			custom_value = input(colors.wy+" "+translations['inserisci_numero_cicli']+" "+colors.gr)
			if custom_value.isdigit() and int(custom_value) > 0:
				ca_ripet = custom_value + " " + translations['cicli']
				break
			else:
				print(colors.re+" "+translations['valore_non_valido'])

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_ripet",ca_ripet)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetContinuousAddingRipet()


def SetContinuousAddingPause():
	log = getSetting('log','general_settings')

	ca_pause = getSetting('ca_pause','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_cicli_ca_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_cicli_ca_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_cicli_ca_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_cicli_ca_cap_txt_3'])
	print(colors.wy+" "+translations['pausa_cicli_ca_cap_txt_4'])
	print(colors.wy+" "+translations['pausa_cicli_ca_cap_txt_5'])
	print(colors.wy+" "+translations['pausa_cicli_ca_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+translations['nessuna_pausa'])
	print(colors.cy+" 13 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1' or choise == '2' or choise == '3':
		ca_pause = int(choise)*60
		ca_pause = str(ca_pause)+" "+translations['abbreviazione_secondi']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",ca_pause)
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '4' or choise == '5' or choise == '6':
		if choise == '4':
			ca_pause = '300 '+translations['abbreviazione_secondi']
		elif choise == '5':
			ca_pause = '600 '+translations['abbreviazione_secondi']
		elif choise == '6':
			ca_pause = '900 '+translations['abbreviazione_secondi']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",ca_pause)
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '7':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",'1800 '+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '8':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",'3600 '+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '9':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",'7200 '+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '10':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",'21600 '+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '11':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",'43200 '+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()


	elif choise == '12':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '13':
		while True:
			print()
			custom_value = input(colors.wy+" "+translations['inserisci_pausa_secondi']+" "+colors.gr)
			if custom_value.isdigit() and int(custom_value) > 0:
				ca_pause = custom_value + " " + translations['abbreviazione_secondi']
				break
			else:
				print(colors.re+" "+translations['valore_non_valido'])

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","ca_pause",ca_pause)
		config.write(cnfFile)
		cnfFile.close()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		
		SetContinuousAddingPause()

	if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

	menu.AddingSettingsMenu()


def SetIfNotIn():
	log = getSetting('log','general_settings')

	if_account_out = getSetting('if_account_out','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['autoinvito_automatico_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['autoinvito_automatico_cap_txt_1'])
	print(colors.wy+" "+translations['autoinvito_automatico_cap_txt_2'])
	print(colors.wy+" "+translations['autoinvito_automatico_cap_txt_3'])
	print(colors.wy+" "+translations['autoinvito_automatico_cap_txt_4'])
	print(colors.wy+" "+translations['autoinvito_automatico_cap_txt_5'])
	print(colors.wy+" "+translations['autoinvito_automatico_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","if_account_out",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","if_account_out",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetIfNotIn()

def SetChangeEveryNAdded(add_custom_option=False):
	log = getSetting('log','general_settings')

	change_account_n_requests = getSetting('change_account_n_requests','adding_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['limite_richieste_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['limite_richieste_cap_txt_1'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_2'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_3'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_4'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_5'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()

	if add_custom_option:
		print(colors.cy+"  0 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print(colors.cy+"  1 | "+colors.wy+"5 "+translations['richieste'])
	print(colors.cy+"  2 | "+colors.wy+"10 "+translations['richieste'])
	print(colors.cy+"  3 | "+colors.wy+"15 "+translations['richieste'])
	print(colors.cy+"  4 | "+colors.wy+"20 "+translations['richieste'])
	print(colors.cy+"  5 | "+colors.wy+"25 "+translations['richieste'])
	print(colors.cy+"  6 | "+colors.wy+"30 "+translations['richieste'])
	print(colors.cy+"  7 | "+colors.wy+"35 "+translations['richieste'])
	print(colors.cy+"  8 | "+colors.wy+"40 "+translations['richieste'])
	print(colors.cy+"  9 | "+colors.wy+"45 "+translations['richieste'])
	print(colors.cy+" 10 | "+colors.wy+"50 "+translations['richieste'])
	print(colors.cy+" 11 | "+colors.wy+"55 "+translations['richieste'])
	print(colors.cy+" 12 | "+colors.wy+"60 "+translations['richieste'])
	print(colors.cy+" 13 | "+colors.wy+"65 "+translations['richieste'])
	print(colors.cy+" 14 | "+colors.wy+"70 "+translations['richieste'])
	print(colors.cy+" 15 | "+colors.wy+"75 "+translations['richieste'])
	print(colors.cy+" 16 | "+colors.wy+"80 "+translations['richieste'])
	print(colors.cy+" 17 | "+colors.wy+"85 "+translations['richieste'])
	print(colors.cy+" 18 | "+colors.wy+"90 "+translations['richieste'])
	print(colors.cy+" 19 | "+colors.wy+"95 "+translations['richieste'])
	print(colors.cy+" 20 | "+colors.wy+"100 "+translations['richieste'])
	print(colors.cy+" 21 | "+colors.wy+translations['nessun_limite'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	if add_custom_option and choise == '0':
		
		SetCustomIntegerValue('change_account_n_requests', 'adding_settings', translations['richieste'])
		return

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetChangeEveryNAdded(add_custom_option)

	if int(choise) < 21:
		value = 5*int(choise)
		value = str(value)+" "+translations['richieste']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_n_requests",value)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '21':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_n_requests",translations['nessun_limite'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetChangeEveryNAdded(add_custom_option)


def SetBetweenJoinPause():
	log = getSetting('log','general_settings')

	between_autoinvite_pause = getSetting('between_autoinvite_pause','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_ingresso_invito_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_ingresso_invito_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_ingresso_invito_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_ingresso_invito_cap_txt_3'])
	print(colors.wy+" "+translations['pausa_ingresso_invito_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"3-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-60 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-180 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-300 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-600 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-900 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBetweenJoinPause()

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_autoinvite_pause",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif int(choise) <= 10:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_autoinvite_pause",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif int(choise) > 10 and int(choise) < 20:
		if int(choise) == 11:
			value = "120"
		elif int(choise) == 12:
			value = "180"
		elif int(choise) == 13:
			value = "300"
		elif int(choise) == 14:
			value = "600"
		elif int(choise) == 15:
			value = "900"
		elif int(choise) == 16:
			value = "1800"
		elif int(choise) == 17:
			value = "3600"
		elif int(choise) == 18:
			value = "7200"
		elif int(choise) == 19:
			value = "21600"
		elif int(choise) == 20:
			value = "43200"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_autoinvite_pause",value + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif int(choise) >= 20 and int(choise) < 33:
		if int(choise) == 21:
			value = "0-3"
		elif int(choise) == 22:
			value = "1-3"
		elif int(choise) == 23:
			value = "1-5"
		elif int(choise) == 24:
			value = "1-10"
		elif int(choise) == 25:
			value = "3-5"
		elif int(choise) == 26:
			value = "3-10"
		elif int(choise) == 27:
			value = "3-60"
		elif int(choise) == 28:
			value = "3-120"
		elif int(choise) == 29:
			value = "3-180"
		elif int(choise) == 30:
			value = "3-300"
		elif int(choise) == 31:
			value = "3-600"
		elif int(choise) == 32:
			value = "3-900"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_autoinvite_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif choise == '33':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_autoinvite_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBetweenJoinPause()

def SetBetweenInvitePause():
	log = getSetting('log','general_settings')

	between_invite_pause = getSetting('between_invite_pause','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_ingresso_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_ingresso_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_ingresso_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_ingresso_cap_txt_3'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"1-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"3-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-60 sec ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-120 sec ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-180 sec ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-300 sec ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-600 sec ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-900 sec ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBetweenInvitePause()

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_invite_pause",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif int(choise) <= 10:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_invite_pause",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif int(choise) > 10 and int(choise) < 20:
		if int(choise) == 11:
			value = "120"
		elif int(choise) == 12:
			value = "180"
		elif int(choise) == 13:
			value = "300"
		elif int(choise) == 14:
			value = "600"
		elif int(choise) == 15:
			value = "900"
		elif int(choise) == 16:
			value = "1800"
		elif int(choise) == 17:
			value = "3600"
		elif int(choise) == 18:
			value = "7200"
		elif int(choise) == 19:
			value = "21600"
		elif int(choise) == 20:
			value = "43200"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_invite_pause",value + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif int(choise) >= 20 and int(choise) < 33:
		if int(choise) == 21:
			value = "0-3"
		elif int(choise) == 22:
			value = "1-3"
		elif int(choise) == 23:
			value = "1-5"
		elif int(choise) == 24:
			value = "1-10"
		elif int(choise) == 25:
			value = "3-5"
		elif int(choise) == 26:
			value = "3-10"
		elif int(choise) == 27:
			value = "3-60"
		elif int(choise) == 28:
			value = "3-120"
		elif int(choise) == 29:
			value = "3-180"
		elif int(choise) == 30:
			value = "3-300"
		elif int(choise) == 31:
			value = "3-600"
		elif int(choise) == 32:
			value = "3-900"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_invite_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	elif choise == '33':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","between_invite_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.SettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBetweenInvitePause()

def SetPauseBetweenAccounts(add_custom_option=False):
	log = getSetting('log','general_settings')

	change_account_pause = getSetting('change_account_pause','adding_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_prossimo_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_ingresso_invito_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_prossimo_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_prossimo_cap_txt_3'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()

	if add_custom_option:
		print(colors.cy+"  0 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"3-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-60 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-180 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-300 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-600 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-900 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	if add_custom_option and choise == '0':
		SetCustomPause('change_account_pause', 'adding_settings', True)
		return

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetPauseBetweenAccounts(add_custom_option)

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) <= 20:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60
		elif int(choise) == 11:
			value = 120
		elif int(choise) == 12:
			value = 180
		elif int(choise) == 13:
			value = 300
		elif int(choise) == 14:
			value = 600
		elif int(choise) == 15:
			value = 900
		elif int(choise) == 16:
			value = 1800
		elif int(choise) == 17:
			value = 3600
		elif int(choise) == 18:
			value = 7200
		elif int(choise) == 19:
			value = 21600
		elif int(choise) == 20:
			value = 43200

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) >= 21 and int(choise) < 33:
		if int(choise) == 21:
			value = "0-3"
		elif int(choise) == 22:
			value = "1-3"
		elif int(choise) == 23:
			value = "1-5"
		elif int(choise) == 24:
			value = "1-10"
		elif int(choise) == 25:
			value = "3-5"
		elif int(choise) == 26:
			value = "3-10"
		elif int(choise) == 27:
			value = "3-60"
		elif int(choise) == 28:
			value = "3-120"
		elif int(choise) == 29:
			value = "3-180"
		elif int(choise) == 30:
			value = "3-300"
		elif int(choise) == 31:
			value = "3-600"
		elif int(choise) == 32:
			value = "3-900"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '33':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetPauseBetweenAccounts(add_custom_option)


def SetAutoInvitePause(add_custom_option=False):
	log = getSetting('log','general_settings')

	between_autoinvite_pause = getSetting('between_autoinvite_pause',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_ingresso_auto_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_ingresso_auto_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_ingresso_auto_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_ingresso_auto_cap_txt_3'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()

	if add_custom_option:
		print(colors.cy+"  0 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"1-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"3-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-60 sec ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-120 sec ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-180 sec ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-300 sec ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-600 sec ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-900 sec ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	if add_custom_option and choise == '0':
		SetCustomPause('between_autoinvite_pause', 'adding_settings', True)
	elif choise.isdigit():

		try:
			int(choise)
		except:
			SetBetweenInvitePause()

		if int(choise) <= 5:
			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8")  
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","between_autoinvite_pause",choise + " "+translations['abbreviazione_secondi'])
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			menu.AddingSettingsMenu()

		elif int(choise) <= 10:
			if int(choise) == 6:
				value = 10
			elif int(choise) == 7:
				value = 15
			elif int(choise) == 8:
				value = 20
			elif int(choise) == 9:
				value = 30
			elif int(choise) == 10:
				value = 60

			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8")  
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","between_autoinvite_pause",str(value) + " "+translations['abbreviazione_secondi'])
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			menu.AddingSettingsMenu()

		elif int(choise) > 10 and int(choise) < 20:
			if int(choise) == 11:
				value = "120"
			elif int(choise) == 12:
				value = "180"
			elif int(choise) == 13:
				value = "300"
			elif int(choise) == 14:
				value = "600"
			elif int(choise) == 15:
				value = "900"
			elif int(choise) == 16:
				value = "1800"
			elif int(choise) == 17:
				value = "3600"
			elif int(choise) == 18:
				value = "7200"
			elif int(choise) == 19:
				value = "21600"
			elif int(choise) == 20:
				value = "43200"

			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8")  
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","between_autoinvite_pause",value + " "+translations['abbreviazione_secondi'])
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			menu.AddingSettingsMenu()

		elif int(choise) >= 20 and int(choise) < 33:
			if int(choise) == 21:
				value = "0-3"
			elif int(choise) == 22:
				value = "1-3"
			elif int(choise) == 23:
				value = "1-5"
			elif int(choise) == 24:
				value = "1-10"
			elif int(choise) == 25:
				value = "3-5"
			elif int(choise) == 26:
				value = "3-10"
			elif int(choise) == 27:
				value = "3-60"
			elif int(choise) == 28:
				value = "3-120"
			elif int(choise) == 29:
				value = "3-180"
			elif int(choise) == 30:
				value = "3-300"
			elif int(choise) == 31:
				value = "3-600"
			elif int(choise) == 32:
				value = "3-900"

			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8")  
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","between_autoinvite_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			menu.AddingSettingsMenu()

		elif choise == '33':
			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8")  
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","between_autoinvite_pause",translations['nessuna_pausa'])
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBetweenInvitePause(add_custom_option)


def SetCustomPause(setting_name, section, allow_range):
	print()
	print(colors.wm + colors.wy + " " + translations['set_custom_pause'] + " " + colors.wreset)
	print()
	print(colors.wy + " " + translations['enter_pause_value'])
	if allow_range:
		print(colors.wy + " " + translations['enter_range_example'])
	print()
	print(colors.cy + " " + translations['premi_q_indietro'])
	print()
	
	while True:
		value = input(colors.cy + " " + translations['digita_tua_scelta_arrow'] + " " + colors.gr)
		
		if value.lower() == 'q':
			return
		
		if '-' in value and allow_range:
			try:
				start, end = map(int, value.split('-'))
				if start < end:
					value = f"{start}-{end} {translations['abbreviazione_secondi']} ({translations['casuale']})"
					break
			except ValueError:
				print(colors.re + " " + translations['invalid_input'])
		elif value.isdigit():
			value = f"{value} {translations['abbreviazione_secondi']}"
			break
		else:
			print(colors.re + " " + translations['invalid_input'])
	
	config = configparser.ConfigParser()
	config.read('data/settings.data', encoding="UTF-8")
	cnfFile = open('data/settings.data', "w", encoding="UTF-8")
	config.set(section, setting_name, value)
	config.write(cnfFile)
	cnfFile.close()

	print(colors.gr + " " + translations['setting_updated'])


def SetStopMaxAdding():
	log = getSetting('log','general_settings')

	stop_max_adding = getSetting('stop_max_adding',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['limite_aggiunte_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_1'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_2'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_3'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_4'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_5'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_6'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_7'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+translations['inserisci_valore'])
	print(colors.cy+"  2 | "+colors.wy+translations['nessun_limite'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetStopMaxAdding()
	
	if int(choise) == 1:
		print()
		print(" "+translations['inserisci_massimo_utenti'])
		choise_num = menu.setChoise()

		try:
			value = int(choise_num)
			value = str(value)+" "+translations['utenti']
			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8") 
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","stop_max_adding",value)
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			menu.AddingSettingsMenu()
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			SetStopMaxAdding()	

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","stop_max_adding",translations['nessun_limite'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetStopMaxAdding()


def SetConsecutiveErrorsBreaker(add_custom_option=False):
	log = getSetting('log','general_settings')

	consecutive_error_breaker = getSetting('consecutive_error_breaker',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['limite_errori_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['limite_errori_cap_txt_1'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_2'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_3'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_4'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_5'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_6'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_7'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()

	if add_custom_option:
		print(colors.cy+"  0 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print(colors.cy+"  1 | "+colors.wy+""+colors.wy+"1 "+translations['errore'])
	print(colors.cy+"  2 | "+colors.wy+""+colors.wy+"2 "+translations['errori'])
	print(colors.cy+"  3 | "+colors.wy+""+colors.wy+"3 "+translations['errori'])
	print(colors.cy+"  4 | "+colors.wy+""+colors.wy+"4 "+translations['errori'])
	print(colors.cy+"  5 | "+colors.wy+""+colors.wy+"5 "+translations['errori'])
	print(colors.cy+"  6 | "+colors.wy+""+colors.wy+"10 "+translations['errori'])
	print(colors.cy+"  7 | "+colors.wy+""+colors.wy+"15 "+translations['errori'])
	print(colors.cy+"  8 | "+colors.wy+""+colors.wy+"20 "+translations['errori'])
	print(colors.cy+"  9 | "+colors.wy+""+colors.wy+"25 "+translations['errori'])
	print(colors.cy+" 10 | "+colors.wy+""+colors.wy+"30 "+translations['errori'])
	print(colors.cy+" 11 | "+colors.wy+""+colors.wy+"35 "+translations['errori'])
	print(colors.cy+" 12 | "+colors.wy+""+colors.wy+"40 "+translations['errori'])
	print(colors.cy+" 13 | "+colors.wy+""+colors.wy+"45 "+translations['errori'])
	print(colors.cy+" 14 | "+colors.wy+""+colors.wy+"50 "+translations['errori'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	if add_custom_option and choise == '0':
		SetCustomIntegerValue('consecutive_error_breaker', 'adding_settings', translations['errori'])
		return

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetConsecutiveErrorsBreaker(add_custom_option)

	if int(choise) < 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","consecutive_error_breaker",str(choise)+" "+translations['errori'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) >= 5 and int(choise) <= 14:
		value = (int(choise)-4)*5

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","consecutive_error_breaker",str(value)+" "+translations['errori'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetConsecutiveErrorsBreaker(add_custom_option)

def SetCustomIntegerValue(setting_name, section, unit):
	log = getSetting('log','general_settings')
	print()
	print(colors.wm + colors.wy + " " + translations['set_custom_value'] + " " + colors.wreset)
	print()
	print(colors.wy + " " + translations['enter_value'])
	print()
	print(colors.cy + " " + translations['premi_q_indietro'])
	print()
	
	while True:
		value = input(colors.cy + " " + translations['digita_tua_scelta_arrow'] + " " + colors.gr)
		
		if value.lower() == 'q':
			return
		
		if value.isdigit():
			if unit:
				value = f"{value} {unit}"
			break
		else:
			print(colors.re + " " + translations['invalid_input'])
	
	config = configparser.ConfigParser()
	config.read('data/settings.data', encoding="UTF-8")
	cnfFile = open('data/settings.data', "w", encoding="UTF-8")
	config.set(section, setting_name, value)
	config.write(cnfFile)
	cnfFile.close()

	print(colors.gr + " " + translations['setting_updated'])

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.AddingSettingsMenu()


def SetStartPoint():
	log = getSetting('log','general_settings')

	start_point_members_file = getSetting('start_point_members_file',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['punto_inizio_membri_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_1'])
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_2'])
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_3'])
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['da_interrotto'])
	print(colors.cy+" 2 | "+colors.wy+translations['da_inizio'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","start_point_members_file",translations['da_interrotto'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","start_point_members_file",translations['da_inizio'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetStartPoint()


def SetAddUsing():
	log = getSetting('log','general_settings')

	add_using = getSetting('add_using','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['seleziona_metodo_aggiunta_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_1'])
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_2'])
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_3'])
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['username_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['id_utente_cap'])
	print(colors.cy+" 3 | "+colors.wy+translations['user_id_opt'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","add_using",translations['username_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","add_using",translations['id_utente_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '3':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","add_using",translations['user_id_opt'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetAddUsing()

def SetAddPause(add_custom_option=False):
	log = getSetting('log','general_settings')

	between_adding_pause = getSetting('between_adding_pause',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['pause_aggiunte_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_1'])
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_2'])
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_3'])
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()

	if add_custom_option:
		print(colors.cy+"  0 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"0-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"1-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-20 sec ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-30 sec ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-60 sec ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-120 sec ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-180 sec ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+"3-300 sec ("+translations['casuale']+")")
	print(colors.cy+" 34 | "+colors.wy+"3-600 sec ("+translations['casuale']+")")
	print(colors.cy+" 35 | "+colors.wy+"3-900 sec ("+translations['casuale']+")")
	print(colors.cy+" 36 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	if add_custom_option and choise == '0':
		SetCustomPause('between_adding_pause', 'adding_settings', True)
		return

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetAddPause(add_custom_option)

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) <= 20:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60
		elif int(choise) == 11:
			value = 120
		elif int(choise) == 12:
			value = 180
		elif int(choise) == 13:
			value = 300
		elif int(choise) == 14:
			value = 600
		elif int(choise) == 15:
			value = 900
		elif int(choise) == 16:
			value = 1800
		elif int(choise) == 17:
			value = 3600
		elif int(choise) == 18:
			value = 7200
		elif int(choise) == 19:
			value = 21600
		elif int(choise) == 20:
			value = 43200

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) > 20 and int(choise) < 36:
		if int(choise) == 21:
			value = "0-3"
		elif int(choise) == 22:
			value = "0-5"
		elif int(choise) == 23:
			value = "1-3"
		elif int(choise) == 24:
			value = "1-5"
		elif int(choise) == 25:
			value = "1-10"
		elif int(choise) == 26:
			value = "3-5"
		elif int(choise) == 27:
			value = "3-10"
		elif int(choise) == 28:
			value = "3-20"
		elif int(choise) == 29:
			value = "3-30"
		elif int(choise) == 30:
			value = "3-60"
		elif int(choise) == 31:
			value = "3-120"
		elif int(choise) == 32:
			value = "3-180"
		elif int(choise) == 33:
			value = "3-300"
		elif int(choise) == 34:
			value = "3-600"
		elif int(choise) == 35:
			value = "3-900"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '36':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetAddPause(add_custom_option)

def SetRandomPause(add_custom_option=False):
	log = getSetting('log','general_settings')

	casual_pause_times = getSetting('casual_pause_times',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_casuale_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_3'])
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()

	if add_custom_option:
		print(colors.cy+"  0 | "+colors.wy+translations['inserisci_valore_personalizzato'])

	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"0-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 13 | "+colors.wy+"0-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 14 | "+colors.wy+"1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 15 | "+colors.wy+"1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 16 | "+colors.wy+"1-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 17 | "+colors.wy+"3-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 18 | "+colors.wy+"3-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 19 | "+colors.wy+"3-20 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 20 | "+colors.wy+"3-30 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 21 | "+colors.wy+"3-60 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()
	
	if add_custom_option and choise == '0':
		SetCustomPause('casual_pause_times', 'adding_settings', True)
		return

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetRandomPause(add_custom_option)

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) <= 11:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60
		elif int(choise) == 11:
			value = 120

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) > 11 and int(choise) < 23:
		if int(choise) == 12:
			value = "0-3"
		elif int(choise) == 13:
			value = "0-5"
		elif int(choise) == 14:
			value = "1-3"
		elif int(choise) == 15:
			value = "1-5"
		elif int(choise) == 16:
			value = "1-10"
		elif int(choise) == 17:
			value = "3-5"
		elif int(choise) == 18:
			value = "3-10"
		elif int(choise) == 19:
			value = "3-20"
		elif int(choise) == 20:
			value = "3-30"
		elif int(choise) == 21:
			value = "3-60"
		elif int(choise) == 22:
			value = "3-120"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '23':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetRandomPause(add_custom_option)


def SetBotFilter():
	log = getSetting('log','general_settings')

	exclude_bot = getSetting('exclude_bot','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['escludi_bot_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['escludi_bot_cap_txt_1'])
	print(colors.wy+" "+translations['escludi_bot_cap_txt_2'])
	print(colors.wy+" "+translations['escludi_bot_cap_txt_3'])
	print(colors.wy+" "+translations['escludi_bot_cap_txt_4'])
	print(colors.wy+" "+translations['escludi_bot_cap_txt_5'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","exclude_bot",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","exclude_bot",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetBotFilter()

def SetAdminFilter():
	log = getSetting('log','general_settings')

	exclude_admin = getSetting('exclude_admin','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['escludi_admin_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['escludi_admin_cap_txt_1'])
	print(colors.wy+" "+translations['escludi_admin_cap_txt_2'])
	print(colors.wy+" "+translations['escludi_admin_cap_txt_3'])
	print(colors.wy+" "+translations['escludi_admin_cap_txt_4'])
	print(colors.wy+" "+translations['escludi_admin_cap_txt_5'])
	print(colors.wy+" "+translations['escludi_admin_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro']+"  ")
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","exclude_admin",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","exclude_admin",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetAdminFilter()


def SetPictureFilter():
	log = getSetting('log','general_settings')

	photo_forcing = getSetting('photo_forcing','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['filtro_foto_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['filtro_foto_cap_txt_1'])
	print(colors.wy+" "+translations['filtro_foto_cap_txt_2'])
	print(colors.wy+" "+translations['filtro_foto_cap_txt_3'])
	print(colors.wy+" "+translations['filtro_foto_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","photo_forcing",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","photo_forcing",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetPictureFilter()


def SetLastSeenFilter():
	log = getSetting('log','general_settings')

	filter_last_seen = getSetting('filter_last_seen','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['filtro_accesso_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['filtro_accesso_cap_txt_1'])
	print(colors.wy+" "+translations['filtro_accesso_cap_txt_2'])
	print(colors.wy+" "+translations['filtro_accesso_cap_txt_3'])
	print(colors.wy+" "+translations['filtro_accesso_cap_txt_4'])
	print(colors.wy+" "+translations['filtro_accesso_cap_txt_5'])
	print(colors.wy+" "+translations['filtro_accesso_cap_txt_6'])
	print()
	print(colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['filtro_accesso_1'])
	print(colors.cy+" 2 | "+colors.wy+translations['filtro_accesso_2'])
	print(colors.cy+" 3 | "+colors.wy+translations['filtro_accesso_3'])
	print(colors.cy+" 4 | "+colors.wy+translations['filtro_accesso_4'])
	print(colors.cy+" 5 | "+colors.wy+translations['filtro_accesso_5'])
	print(colors.cy+" 6 | "+colors.wy+translations['nessuna_restrizione'])
	print()
	print(colors.cy+" q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_last_seen",translations['filtro_accesso_1'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_last_seen",translations['filtro_accesso_2'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '3':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_last_seen",translations['filtro_accesso_3'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '4':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_last_seen",translations['filtro_accesso_4'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '5':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_last_seen",translations['filtro_accesso_5'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '6':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_last_seen",translations['nessuna_restrizione'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetLastSeenFilter()

def setDCEnabled():
	print()
	print(colors.gr+" "+translations['inserisci_dc_ammessi_1'])
	print(colors.cy+" "+translations['inserisci_dc_ammessi_2'])
	print(" ----------------------------")
	choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)

	if choise != 'q':
		numbers = re.findall(r'\d+', choise) 
		str_dc = ''
		i = 0

		for x in numbers:
			if i > 0:
				str_dc = str_dc + '-' + str(x)
			else:
				str_dc = str(x)

			i = i+1
	else:
		str_dc = 'q'

	return str_dc


def SetDCFilter():
	log = getSetting('log','general_settings')

	filter_dc = getSetting('filter_dc','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['filtro_dc_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['filtro_dc_cap_txt_1'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_2'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_3'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_4'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_5'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_6'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_7'])
	print(colors.wy+" "+translations['filtro_dc_cap_txt_8'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['inserisci_lista_dc_ammessi'])
	print(colors.cy+" 2 | "+colors.wy+translations['nessuna_restrizione'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		choise = setDCEnabled()
		if choise != 'q':
			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8")  
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","filter_dc",choise)
			config.write(cnfFile)
			cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_dc",translations['nessuna_restrizione'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetDCFilter()


def SetPhoneFilter():
	log = getSetting('log','general_settings')

	filter_phone_number = getSetting('filter_phone_number','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['filtro_tel_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['filtro_tel_cap_txt_1'])
	print(colors.wy+" "+translations['filtro_tel_cap_txt_2'])
	print(colors.wy+" "+translations['filtro_tel_cap_txt_3'])
	print(colors.wy+" "+translations['filtro_tel_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_phone_number",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","filter_phone_number",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetPhoneFilter()

