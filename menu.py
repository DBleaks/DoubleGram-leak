import configparser, csv, os, sys, colors, settings, banner
from voip import ManageAccountList, AnalyzeAccounts, ShowServiceMessages, EditAccount, DeleteAccount, LeaveGroupChannel, AutoJoinGroup, OpenStatusPrivacySettings, CloseStatusPrivacySettings, InviteInGroup, OpenChatInvitePrivacySettings, CloseChatInvitePrivacySettings, SetVoipsAsAdmin, UnsetVoipsAsAdmin, OpenPhoneNumberPrivacySettings, ClosePhoneNumberPrivacySettings, OpenForwardLinkPrivacySettings, CloseForwardLinkPrivacySettings, OpenProfilePicturePrivacySettings, CloseProfilePicturePrivacySettings, OpenIncomingCallsPrivacySettings, CloseIncomingCallsPrivacySettings, UpdateUsernameSettings, UpdateBioSettings, UpdateNameSettings, UpdateSurnameSettings
from members import AddMembers, RewriteMembers
from adding import AddUsers, RemoveLastAddedUsers

colors.getColors()

log = settings.getSetting('log','general_settings')

translations = {}

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
	print(' 1 | Engligh')
	print(' 2 | Italiano')
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

if log != translations['disabilitato_first_cap'] and log != translations['abilitato_first_cap']:
	log = translations['disabilitato_first_cap']
	
def setChoise():
	print(colors.cy+" "+translations['set_choise_line'])
	choise = input(colors.cy+" "+translations['set_choise_txt']+colors.gr)
	
	return choise


def continueToPrincipal():
	print(colors.cy+translations['continue_principal_line'])
	choise = input(colors.cy+translations['continue_principal_txt']+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	PrincipalMenu()


def PrincipalMenu(show_menu=True):
	if show_menu == True:
		log = settings.getSetting('log','general_settings')

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
	else:
		log = settings.getSetting('log','general_settings')
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

	cpass = configparser.RawConfigParser()
	
	try:
		with open('data/config.data', encoding="UTF-8") as f:
			cpass.read_file(f)
			
			print()
			print(colors.cy+translations['menu_principale_line'])
			print(colors.cy+translations['menu_principale_text'])
			print(colors.cy+translations['menu_principale_line'])
			print(colors.wm+colors.wy+" - "+translations['account_plurale_cap']+" "+colors.wreset)

			print(colors.cy+"  1 | "+colors.wy+translations['aggiungi_account'])
			print(colors.cy+"  2 | "+colors.wy+translations['gestione_account'])
			print(colors.cy+"  3 | "+colors.wy+translations['analisi_account'])
			print(colors.wm+colors.wy+" - "+translations['membri_cap']+" "+colors.wreset)
			print(colors.cy+"  4 | "+colors.wy+translations['preleva_da'])
			print(colors.wm+colors.wy+" - "+translations['adding_cap']+" "+colors.wreset)
			print(colors.cy+"  5 | "+colors.wy+translations['centro_adding'])
			print(colors.wm+colors.wy+" - "+translations['altro_cap']+" "+colors.wreset)
			print(colors.cy+"  6 | "+colors.wy+translations['impostazioni'])
			print(colors.cy+"  7 | "+colors.wy+translations['impostazioni_scraping'])
			print(colors.cy+"  8 | "+colors.wy+translations['impostazioni_adding'])
			
			print()
			print(colors.cy+"  9 | "+translations['esci'])

			print(colors.wreset)
			
			try:
				choise = int(setChoise())
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				PrincipalMenu()

	except IOError:
		PrincipalMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ManageAccountList(1)
		
	elif choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		MembersMenu()

	elif choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ManageAccounts()

	elif(choise == 3):
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AnalyzeAccounts()

	elif(choise == 5):
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingMenu()

	elif(choise == 6):
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SettingsMenu()

	elif(choise == 7):
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ScrapingSettings()

	elif(choise == 8):
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingSettingsMenu()

	elif(choise == 9):
		print(colors.wreset)
		sys.exit()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		PrincipalMenu()


def MembersMenu():


	# Check if there is a members.csv file, if not create it
	if not os.path.isfile('members/members.csv'):
		with open("members/members_temp.csv","w",encoding='UTF-8') as f:
			writer = csv.writer(f,delimiter=",",lineterminator="\n")
			writer.writerow(['username','user id', 'access hash', 'name', 'group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated', 'is_premium'])

	if not os.path.isfile('members/members_temp.csv'):
		with open("members/members_temp.csv","w",encoding='UTF-8') as f:
			writer = csv.writer(f,delimiter=",",lineterminator="\n")
			writer.writerow(['username','user id', 'access hash', 'name', 'group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated', 'is_premium'])

	# If members.csv doesn't have is_premium in the header, add it and set all values to False
	with open('members/members.csv', encoding='UTF-8') as f:
		csv_reader = csv.reader(f, delimiter=',')
		header = next(csv_reader)
		if 'is_premium' not in header:
			with open('members/members.csv', 'w', encoding='UTF-8') as f:
				writer = csv.writer(f, delimiter=',', lineterminator='\n')
				writer.writerow(header + ['is_premium'])
				for row in csv_reader:
					writer.writerow(row + ['False'])

	
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
				settings.set("scraping_settings", "stop_deep_search_percentage_status", "Disabled")
				settings.set("scraping_settings", "deep_search_pause", "0.50 "+translations['abbreviazione_secondi'])

				setup = open("data/settings.data", "a", encoding="utf-8")
				settings.write(setup)
				setup.close()
	
	except IOError:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		result = settings.checkSettings(True)
		print(colors.wy+" "+translations['impostazioni_base_configurate'])
		MembersMenu()
		
	choise = 1
	cpass = configparser.RawConfigParser()
	
	try:
		with open(r"members/members.csv", encoding='UTF-8') as f:
			users = []
			users_final = []
			num_users = 0
			num_bot = 0
			num_admin = 0
			num_not_photo = 0
			num_phone = 0

			i = 0

			with open(r"members/members.csv", encoding='UTF-8') as f:  
				rows = csv.reader(f,delimiter=",",lineterminator="\n")
				next(rows, None)
				for row in rows:
					num_users = num_users + 1

					if row[6] == 'True':
						num_bot = num_bot + 1

					if row[7] == 'True':
						num_admin = num_admin + 1

					if row[9] == 'False':
						num_not_photo = num_not_photo + 1

					if row[10] != 'False':
						num_phone = num_phone + 1
			print()
			print(colors.cy+translations['preleva_line'])
			print(colors.cy+translations['preleva_txt'])
			print(colors.cy+translations['preleva_line'])
			
			print()
			print("  "+translations['lista_attuale_include'])
			print()
			print("  "+colors.wm+colors.wy+translations['numero_utenti']+":"+str(int(num_users))+colors.wreset, end='')
			print("  "+colors.wm+colors.wy+translations['numero_bot']+":"+str(num_bot)+colors.wreset)
			print()
			print("  "+colors.wm+colors.wy+translations['numero_admin']+":"+str(num_admin)+colors.wreset, end='')
			print("  "+colors.wm+colors.wy+translations['numero_senza_foto']+":"+str(num_not_photo)+colors.wreset)
			print()
			print("  "+colors.wm+colors.wy+translations['numero_telefono_visibile']+":"+str(num_phone)+colors.wreset)
			print()

			print(colors.cy+"  1 | "+colors.wy+translations['seleziona_account_e']+" "+colors.re+translations['sovrascrivi']+colors.wy+" "+translations['la_lista_attuale'])
			print(colors.cy+"  2 | "+colors.wy+translations['seleziona_account_e']+" "+colors.re+translations['aggiungi']+colors.wy+" "+translations['alla_lista_attuale'])
			print(colors.cy+"  3 | "+colors.wy+translations['impostazioni_scraping'])
			print(colors.cy+"  4 | "+colors.wy+translations['procedi_adding'])
			print()
			print(colors.cy+"  q | <- "+translations['torna_menu_principale'])
			choise = setChoise()

			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				PrincipalMenu()

			try:
				choise = int(choise)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				MembersMenu()

			if choise == 1:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				SelectScrapingMethod(translations['opt_overwrite'])

			elif choise == 4:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				AddingMenu()

			elif choise == 2:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				SelectScrapingMethod(translations['opt_add_to'])

			elif choise == 3:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				ScrapingSettings()

			else:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				MembersMenu()

	except IOError:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		MembersMenu()


def ScrapingSettings():
	# CHeck if deep_search_characters is in settings.data
	settings.checkSettings(True)
	
	stop_deep_search_percentage = settings.getSetting('stop_deep_search_percentage','scraping_settings')
	stop_deep_search_percentage_status = settings.getSetting('stop_deep_search_percentage_status','scraping_settings')
	blacklist_status = settings.getSetting('blacklist_status','scraping_settings')
	deep_search_pause = settings.getSetting('deep_search_pause','scraping_settings')


	print()
	print(colors.cy+translations['imp_scraping_line'])
	print(colors.cy+translations['imp_scraping_txt'])
	print(colors.cy+translations['imp_scraping_line'])
	print(colors.wm+colors.wy+" - "+translations['imp_deep_search']+" "+colors.wreset)
	print(colors.cy+"  1 | "+colors.wy+translations['choose_characters']+colors.wreset)
	
	print(colors.cy+"  2 | "+colors.wy+translations['pause_between_requests']+": "+colors.wreset + colors.cy+deep_search_pause+colors.wreset)
	print(colors.cy+"  3 | "+colors.wy+translations['stop_until_reached']+": "+colors.wreset + colors.cy+stop_deep_search_percentage+"%"+colors.wreset)
	print(colors.cy+"  4 | "+colors.wy+translations['stop_until_reached_status']+": "+colors.wreset + colors.cy+stop_deep_search_percentage_status+colors.wreset)
	print(colors.wm+colors.wy+" - "+translations['imp_blacklist']+" "+colors.wreset)
	print(colors.cy+"  5 | "+colors.wy+translations['blacklist_status']+": "+colors.wreset+ colors.cy+blacklist_status+colors.wreset)
	print(colors.cy+"  6 | "+colors.wy+translations['aggiungi_blacklist'])
	print(colors.cy+"  7 | "+colors.wy+translations['rimuovi_blacklist'])
	print(colors.wm+colors.wy+" - "+translations['scraping_actions']+" "+colors.wreset)
	print(colors.cy+"  8 | "+colors.wy+translations['remove_duplicates']+colors.wreset)
	print(colors.cy+"  9 | "+colors.wy+translations['remove_blacklisted']+colors.wreset)
	
	print()
	print(colors.cy+"  q | "+translations['premi_q_indietro'])

	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		MembersMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ScrapingSettings()


	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetDeepSearchCharacters()
	
	elif choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetPauseBetweenScrapingRequests()

	elif choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetStopScrapingUntilReached()

	elif choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetStopScrapingUntilReachedStatus()

	elif choise == 5:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetBlacklistStatus()
	
	elif choise == 6:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.AddUserToBlacklist()
	
	elif choise == 7:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.RemoveUserFromBlacklist()
	
	elif choise == 8:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.RemoveDuplicates()
	
	elif choise == 9:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.RemoveBlacklistedUsers()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ScrapingSettings()
		
	
def SelectScrapingMethod(mode): 

	print()
	print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)
	
	print()

	print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+mode+colors.wreset)
	print()
	print(colors.gr+" "+translations['metodo_scraping'])
	print(colors.cy+" "+translations['metodo_scraping_line'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['metodo_1'])
	print(colors.cy+" 2 | "+colors.wy+translations['metodo_2'])
	print(colors.cy+" 3 | "+colors.wy+translations['metodo_3'])
	print()
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		MembersMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SelectScrapingMethod(mode)

	
	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		if mode == translations['opt_overwrite']:
			RewriteMembers('method_1')
		else:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			AddMembers('method_1')

	elif choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		if mode == translations['opt_overwrite']:
			RewriteMembers('method_2')
		else:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			AddMembers('method_2')

	elif choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		if mode == translations['opt_overwrite']:
			RewriteMembers('method_3')
		else:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			AddMembers('method_3')

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SelectScrapingMethod(mode)

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	



def AddingMenu():
	choise = 1
	cpass = configparser.RawConfigParser()
	
	print()
	print(colors.cy+translations['aggiungi_membri_line'])
	print(colors.cy+translations['aggiungi_membri_txt'])
	print(colors.cy+translations['aggiungi_membri_line'])
	print(colors.cy+" 1 | "+colors.wy+translations['scegli_e_avvia'])
	print(colors.cy+" 2 | "+colors.wy+translations['impostazioni_adding'])

	is_last_added = False
	num_users = 0
	try:
		with open(r"members/last_added.csv", encoding='UTF-8') as f:  
			rows = csv.reader(f,delimiter=",",lineterminator="\n")
			next(rows, None)
			for row in rows:
				num_users = num_users + 1
				is_last_added = True
			
			if is_last_added == True:
				print(colors.cy+" 3 | "+colors.wy+translations['rimuovi_utenti_aggiunti'])
	except Exception as e:
		pass

	print()
	print(colors.cy+" q | <- "+translations['torna_menu_principale'])
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		PrincipalMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddUsers(voip_index=None)

	elif choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingSettingsMenu()

	elif choise == 3 and is_last_added == True:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		RemoveLastAddedUsers()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingMenu()


def ManageAccounts():
	choise = 1
	cpass = configparser.RawConfigParser()
	
	print()
	print(colors.cy+translations['gestione_account_line'])
	print(colors.cy+translations['gestione_account_txt'])
	print(colors.cy+translations['gestione_account_line'])
	print(colors.wm+colors.wy+" - "+translations['lista_account_cap']+" "+colors.wreset)
	print(colors.cy+"  1 | "+colors.wy+translations['crea_nuova_lista'])
	print(colors.cy+"  2 | "+colors.wy+translations['abilita_dis_account'])
	print(colors.cy+"  3 | "+colors.wy+translations['scollega_account'])
	print(colors.wm+colors.wy+" - "+translations['invito_ingresso_cap']+" "+colors.wreset)
	print(colors.cy+"  4 | "+colors.wy+translations['invito_tramite_txt'])
	print(colors.cy+"  5 | "+colors.wy+translations['ingresso_automatico_txt'])
	#print(colors.cy+"  6 | Impostazioni invito e ingresso automatico account")
	print(colors.cy+"  6 | "+colors.wy+translations['fai_uscire_txt'])
	print(colors.wm+colors.wy+" - "+translations['privacy_account_cap']+" "+colors.wreset)
	print(colors.cy+"  7 | "+colors.wy+translations['mostra_accesso_tutti'])
	print(colors.cy+"  8 | "+colors.wy+translations['nega_accesso_tutti'])
	print(colors.cy+"  9 | "+colors.wy+translations['permetti_aggiunta_gruppi'])
	print(colors.cy+" 10 | "+colors.wy+translations['nega_aggiunta_gruppi'])
	print(colors.cy+" 11 | "+colors.wy+translations['mostra_telefono_tutti'])
	print(colors.cy+" 12 | "+colors.wy+translations['nega_telefono_tutti'])
	print(colors.cy+" 13 | "+colors.wy+translations['mostra_foto_tutti'])
	print(colors.cy+" 14 | "+colors.wy+translations['nega_foto_tutti'])
	print(colors.cy+" 15 | "+colors.wy+translations['mostra_inoltrati_tutti'])
	print(colors.cy+" 16 | "+colors.wy+translations['nega_inoltrati_tutti'])
	print(colors.cy+" 17 | "+colors.wy+translations['permetti_chiamate_tutti'])
	print(colors.cy+" 18 | "+colors.wy+translations['nega_chiamate_tutti'])
	print(colors.wm+colors.wy+" - "+translations['dati_account_cap']+" "+colors.wreset)
	print(colors.cy+" 19 | "+colors.wy+translations['modifica_username'])
	print(colors.cy+" 20 | "+colors.wy+translations['modifica_nome'])
	print(colors.cy+" 21 | "+colors.wy+translations['modifica_cognome'])
	print(colors.cy+" 22 | "+colors.wy+translations['modifica_biografia'])
	print(colors.wm+colors.wy+" - "+translations['amministratori_cap']+" "+colors.wreset)
	print(colors.cy+" 23 | "+colors.wy+translations['rendi_amministratori'])
	print(colors.cy+" 24 | "+colors.wy+translations['rimuovi_amministratori'])
	print(colors.wm+colors.wy+" - "+translations['messaggi_cap']+" "+colors.wreset)
	print(colors.cy+" 25 | "+colors.wy+translations['mostra_messaggi_servizio'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_menu_principale'])
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		PrincipalMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ManageAccounts()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ManageAccountList(0)

	if choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		EditAccount()

	if choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		InviteInGroup(voip_index=None)

	elif choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		DeleteAccount()

	elif choise == 6:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		LeaveGroupChannel(voip_index=None)

	elif choise == 7:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenStatusPrivacySettings()

	elif choise == 8:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseStatusPrivacySettings()

	elif choise == 9:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenChatInvitePrivacySettings()

	elif choise == 10:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseChatInvitePrivacySettings()

	elif choise == 11:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenPhoneNumberPrivacySettings()

	elif choise == 12:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ClosePhoneNumberPrivacySettings()

	elif choise == 13:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenProfilePicturePrivacySettings()

	elif choise == 14:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseProfilePicturePrivacySettings()

	elif choise == 15:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenForwardLinkPrivacySettings()

	elif choise == 16:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseForwardLinkPrivacySettings()

	elif choise == 17:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenIncomingCallsPrivacySettings()

	elif choise == 18:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseIncomingCallsPrivacySettings()

	elif choise == 19:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		UpdateUsernameSettings(voip_index=None)

	elif choise == 20:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		UpdateNameSettings(voip_index=None)

	elif choise == 21:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		UpdateSurnameSettings(voip_index=None)

	elif choise == 22:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		UpdateBioSettings(voip_index=None)

	elif choise == 23:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SetVoipsAsAdmin(voip_index=None)

	elif choise == 24:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		UnsetVoipsAsAdmin(voip_index=None)

	elif choise == 25:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ShowServiceMessages()

	elif choise == 5:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AutoJoinGroup(voip_index=None)

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ManageAccounts()


def SettingsMenu(close=False):

	choise = 1
	cpass = configparser.RawConfigParser()

	log = settings.getSetting('log','general_settings')
	analyze_account = settings.getSetting('analyze_account','general_settings')
	between_invite_pause = settings.getSetting('between_invite_pause','general_settings')
	between_autoinvite_pause = settings.getSetting('between_autoinvite_pause','general_settings')
	language_set = settings.getLang()
	
	print()
	print(colors.cy+translations['impostazioni_line'])
	print(colors.cy+translations['impostazioni_txt'])
	print(colors.cy+translations['impostazioni_line'])
	print(colors.cy+" 1 | "+colors.wy+translations['mantieni_log']+" " + colors.cy + log)
	print(colors.cy+" 2 | "+colors.wy+translations['utente_analisi']+" " + colors.cy + analyze_account)
	print(colors.cy+" 3 | "+colors.wy+translations['pausa_invito_general']+" " + colors.cy + between_invite_pause)
	print(colors.cy+" 4 | "+colors.wy+translations['pausa_ingresso_general']+" " + colors.cy + between_autoinvite_pause)
	print(colors.cy+" 5 | "+colors.wy+translations['lingua']+" " + colors.cy + language_set)
	print()
	print(colors.cy+" q | <- "+translations['torna_menu_principale'])
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		PrincipalMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SettingsMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetLogs()

	if choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetAnalyzeAccount()

	if choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetBetweenInvitePause()

	if choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetBetweenJoinPause()

	if choise == 5:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetLanguage()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		SettingsMenu()


def AddingSettingsMenu():

	# Check if premium_filter is in adding_settings, if not add it
	settings.checkSettings(if_false_create=True)
	choise = 1
	cpass = configparser.RawConfigParser()

	auto_add_at_start = settings.getSetting('auto_add_at_start','adding_settings')
	if_account_out = settings.getSetting('if_account_out','adding_settings')
	change_account_n_requests = settings.getSetting('change_account_n_requests','adding_settings')
	change_account_pause = settings.getSetting('change_account_pause','adding_settings')
	consecutive_error_breaker = settings.getSetting('consecutive_error_breaker','adding_settings')
	start_point_members_file = settings.getSetting('start_point_members_file','adding_settings')
	add_using = settings.getSetting('add_using','adding_settings')
	between_adding_pause = settings.getSetting('between_adding_pause','adding_settings')
	casual_pause_times = settings.getSetting('casual_pause_times','adding_settings')
	exclude_bot = settings.getSetting('exclude_bot','adding_settings')
	exclude_admin = settings.getSetting('exclude_admin','adding_settings')
	photo_forcing = settings.getSetting('photo_forcing','adding_settings')
	filter_last_seen = settings.getSetting('filter_last_seen','adding_settings')
	filter_dc = settings.getSetting('filter_dc','adding_settings')
	filter_phone_number = settings.getSetting('filter_phone_number','adding_settings')
	between_autoinvite_pause = settings.getSetting('between_autoinvite_pause','adding_settings')
	stop_max_adding = settings.getSetting('stop_max_adding','adding_settings')
	continuous_adding = settings.getSetting('continuous_adding','adding_settings')
	ca_ripet = settings.getSetting('ca_ripet','adding_settings')
	ca_pause = settings.getSetting('ca_pause','adding_settings')
	premium_filter = settings.getSetting('premium_filter','adding_settings')
	
	print()
	print(colors.cy+translations['imp_adding_line'])
	print(colors.cy+translations['imp_adding_txt'])
	print(colors.cy+translations['imp_adding_line'])

	print(colors.wm+colors.wy+" - "+translations['regole_account_cap']+" "+colors.wreset)
	print(colors.cy+"  1 | "+colors.wy+translations['invito_iniziale']+" " + colors.cy + auto_add_at_start) 
	print(colors.cy+"  2 | "+colors.wy+translations['pausa_invito_iniziale']+" " + colors.cy + between_autoinvite_pause) 
	print(colors.cy+"  3 | "+colors.wy+translations['ingresso_iniziale']+" " + colors.cy + if_account_out) 
	print(colors.cy+"  4 | "+colors.wy+translations['cambia_account_ogni']+" " + colors.cy + change_account_n_requests)
	print(colors.cy+"  5 | "+colors.wy+translations['pausa_uso_account']+" " + colors.cy + change_account_pause)
	print(colors.cy+"  6 | "+colors.wy+translations['err_consecutivi']+" " + colors.cy + consecutive_error_breaker)
	
	print(colors.wm+colors.wy+" - "+translations['regole_aggiunte_cap']+" "+colors.wreset)
	print(colors.cy+"  7 | "+colors.wy+translations['punto_inizio']+" " + colors.cy + start_point_members_file)
	print(colors.cy+"  8 | "+colors.wy+translations['aggiungi_tramite']+" " + colors.cy + add_using)
	print(colors.cy+"  9 | "+colors.wy+translations['pausa_aggiunta_altra']+" " + colors.cy + between_adding_pause)
	print(colors.cy+" 10 | "+colors.wy+translations['durata_pausa_casuale']+" " + colors.cy + casual_pause_times)
	print(colors.cy+" 11 | "+colors.wy+translations['blocca_adding_a']+" " + colors.cy + stop_max_adding)
	
	print(colors.wm+colors.wy+" - "+translations['filtri_cap']+" "+colors.wreset)
	print(colors.cy+" 12 | "+colors.wy+translations['escludi_bot_adding']+" " + colors.cy + exclude_bot)
	print(colors.cy+" 13 | "+colors.wy+translations['escludi_admin_adding']+" " + colors.cy + exclude_admin)
	print(colors.cy+" 14 | "+colors.wy+translations['aggiungi_filtro_foto']+" " + colors.cy + photo_forcing)
	print(colors.cy+" 15 | "+colors.wy+translations['aggiungi_accesso_entro']+" " + colors.cy + filter_last_seen)
	print(colors.cy+" 16 | "+colors.wy+translations['aggiungi_filtro_dc']+" " + colors.cy + filter_dc)
	print(colors.cy+" 17 | "+colors.wy+translations['aggiungi_numero_visibile']+" " + colors.cy + filter_phone_number)
	print(colors.cy+" 18 | "+colors.wy+translations['aggiungi_premium']+" " + colors.cy + premium_filter)
	
	print(colors.wm+colors.wy+" - "+translations['ca_cap']+" "+colors.wreset)
	print(colors.cy+" 19 | "+colors.wy+translations['continuous_adding']+" " + colors.cy + continuous_adding)
	print(colors.cy+" 20 | "+colors.wy+translations['ripetizione_adding']+" " + colors.cy + ca_ripet)
	print(colors.cy+" 21 | "+colors.wy+translations['pausa_ciclo_altro']+" " + colors.cy + ca_pause)

	print()
	print(colors.cy+"  q | <- "+translations['centro_adding'])

	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingSettingsMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetAutoInvite()

	if choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetAutoInvitePause(add_custom_option=True)

	if choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetIfNotIn()

	if choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetChangeEveryNAdded(add_custom_option=True)

	if choise == 5:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetPauseBetweenAccounts(add_custom_option=True)

	if choise == 6:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetConsecutiveErrorsBreaker(add_custom_option=True)

	if choise == 7:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetStartPoint()

	if choise == 8:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetAddUsing()

	if choise == 9:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetAddPause(add_custom_option=True)

	if choise == 10:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetRandomPause(add_custom_option=True)

	if choise == 11:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetStopMaxAdding()

	if choise == 12:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetBotFilter()

	if choise == 13:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetAdminFilter()

	if choise == 14:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetPictureFilter()

	if choise == 15:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetLastSeenFilter()

	if choise == 16:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetDCFilter()

	if choise == 17:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetPhoneFilter()

	if choise == 18:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetPremiumFilter()

	if choise == 19:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetContinuousAdding()

	if choise == 20:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetContinuousAddingRipet()

	if choise == 21:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		settings.SetContinuousAddingPause()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		AddingSettingsMenu()