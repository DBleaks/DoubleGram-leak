import os, csv, string, configparser, colors, menu, settings, banner
from voip import AccountSelector, GroupChannelSelector, test_connection, getVoips, activeAnalysis, blockAnalysis
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import functions, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import  InputPeerChannel
import time
import pandas as pd

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

log = settings.getSetting('log','general_settings')

if log != translations['disabilitato_first_cap'] and log != translations['abilitato_first_cap']:
	log = translations['disabilitato_first_cap']

def AddMembers(scraping_method):
	print()
	print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)
	
	print()

	print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+translations['opt_add_to']+colors.wreset+colors.gr+" "+translations['scraping_method']+": "+colors.wm+colors.wy+scraping_method+colors.wreset)

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	try:
		voip_index = AccountSelector(mode='members')
	except e:
		menu.SelectScrapingMethod(translations['opt_add_to'])

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SelectScrapingMethod(translations['opt_add_to'])
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			AddMembers(scraping_method)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		
		voips = getVoips()
		length = len(voips)
		
		if voip_index_mem < 1 or voip_index_mem > length:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			AddMembers(scraping_method)


		voip_index_name = int(voip_index)-1
		voip_name = cpass['credenziali'+str(voip_index_name)]['name']
		
		print()
		print(colors.wm+colors.wy+" "+translations['preleva_e_aggiungi_cap']+" "+colors.wreset)

		print()

		print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+translations['opt_add_to']+colors.wreset+colors.gr+" "+translations['scraping_method']+": "+colors.wm+colors.wy+scraping_method+colors.wreset)
		print()

		print(colors.gr+" "+translations['seleziona_da_cui_prelevare_cap'])
		print(colors.cy+" "+translations['seleziona_da_cui_prelevare_line'])
		
		selected_group = GroupChannelSelector(voip_index)
		if selected_group == 'q' or selected_group == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.AddMembers(scraping_method)
		elif selected_group == False:
			print()
			print(colors.re+" "+translations['impossibile_questo_dest'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			AddMembers(scraping_method)

		else:
			try:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				
				print()
				print(colors.wm+colors.wy+" "+translations['preleva_e_aggiungi_cap']+" "+colors.wreset)

				print()

				print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+translations['opt_add_to']+colors.wreset+colors.gr+" "+translations['scraping_method']+": "+colors.wm+colors.wy+scraping_method+colors.wreset)
				print()

				print(colors.gr+" "+translations['voip_selezionato']+": "+colors.wm+colors.wy+voip_name+colors.wreset+colors.gr+" "+translations['target']+": "+colors.wm+colors.wy+selected_group.title+colors.wreset)
				print()

				scrape_result = ScrapeMethodSelector(voip_index, selected_group, voip_name, scraping_method, mode='Add')
			
			except Exception as e:
				print()
				print(colors.re+" "+translations['impossibile_scaricare_da_destinazione'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				AddMembers(scraping_method)
			
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.MembersMenu()

def RewriteMembers(scraping_method):
	print()
	print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)
	
	print()

	print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+translations['opt_overwrite']+colors.wreset+colors.gr+" "+translations['scraping_method']+": "+colors.wm+colors.wy+scraping_method+colors.wreset)

	
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	
	try:
		voip_index = AccountSelector(mode='members-r')
	except e:
		menu.SelectScrapingMethod(translations['opt_overwrite'])

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.SelectScrapingMethod(translations['opt_overwrite'])
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			RewriteMembers(scraping_method)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		
		voips = getVoips()
		length = len(voips)
		
		if voip_index_mem < 1 or voip_index_mem > length:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			RewriteMembers(scraping_method)


		voip_index_name = int(voip_index)-1
		voip_name = cpass['credenziali'+str(voip_index_name)]['name']
		
		print()
		print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)

		print()

		print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+translations['opt_overwrite']+colors.wreset+colors.gr+" "+translations['scraping_method']+": "+colors.wm+colors.wy+scraping_method+colors.wreset)
		print()

		print(colors.gr+" "+translations['seleziona_da_cui_prelevare_cap'])
		print(colors.cy+" "+translations['seleziona_da_cui_prelevare_line'])
		
		selected_group = GroupChannelSelector(voip_index)
		if selected_group == 'q' or selected_group == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.RewriteMembers(scraping_method)
		elif selected_group == False:
			print()
			print(colors.re+" "+translations['impossibile_questo_dest'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			RewriteMembers(scraping_method)
		else:
			try:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				
				print()
				print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)

				print()

				print(colors.gr+" "+translations['saving_method']+": "+colors.wm+colors.wy+translations['opt_add_to']+colors.wreset+colors.gr+" "+translations['scraping_method']+": "+colors.wm+colors.wy+scraping_method+colors.wreset)
				print()

				print(colors.gr+" "+translations['voip_selezionato']+": "+colors.wm+colors.wy+voip_name+colors.wreset+colors.gr+" "+translations['target']+": "+colors.wm+colors.wy+selected_group.title+colors.wreset)
				print()
				scrape_result = ScrapeMethodSelector(voip_index, selected_group, voip_name, scraping_method, mode='Rewrite')
			except Exception as e:
				print()
				print(colors.re+" "+translations['impossibile_scaricare_da_destinazione'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				RewriteMembers(scraping_method)
			
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.MembersMenu()


def ScrapeMembers(voip_index, selected_group, mode, d, tot_recent_users, channel_connect, client):

	if mode == 'Rewrite':
		method = 'w'
		
	elif mode == 'Add':
		method = 'a'

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = int(voip_index)-1

	if client != False:
		try:
			target_group_entity = client.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))
			is_target = True
		except Exception as e:
			is_target = False
		
		if is_target == True:
			try:
				activeAnalysis()
				all_admin = client.get_participants(target_group_entity, aggressive=False, filter=ChannelParticipantsAdmins)
				blockAnalysis()
			except:
				all_admin = False

			try:
				print(colors.gr+" "+translations['prelevo_membri'])
				all_participants = client.get_participants(target_group_entity, aggressive=False)
				client.disconnect()

			except Exception as e:
				all_participants = False
		else:
			all_participants = False

		if all_participants != False:
			with open("members/members_temp.csv",method,encoding='UTF-8') as f:
				
				print(colors.gr+" "+translations['salvo_membri_in_file'])
				print(colors.gr+" "+translations['attendi'])
				
				writer = csv.writer(f,delimiter=",",lineterminator="\n")
				if method == 'w':
					writer.writerow(['username','user id', 'access hash', 'name', 'group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated', 'is_premium'])
				
				voips = getVoips()

				for user in all_participants:
					found_in_own = False

					for x in voips:
						if x['id'] == str(user.id):
							found_in_own = True

					if found_in_own == False:
						if user.username:
							username = user.username
						else:
							username = ""
						if user.first_name:
							first_name = user.first_name
						else:
							first_name = ""
						if user.last_name:
							last_name = user.last_name
						else:
							last_name = ""
						name = (first_name + ' ' + last_name).strip()

						if user.photo:
							try:
								dc_id = user.photo.dc_id
								have_photo = True
							except:
								dc_id = False
								have_photo = False
						else:
							dc_id = False
							have_photo = False

						if user.bot != False:
							is_bot = True
						else:
							is_bot = False

						if user.phone != None:
							phone = user.phone
						else:
							phone = False

						if user.premium == True:
							is_premium = True
						else:
							is_premium = False

						is_admin = False

						if all_admin != False:
							for admin in all_admin:
								if admin.id == user.id:
									is_admin = True

						writer.writerow([username,user.id,user.access_hash,name,selected_group.title,selected_group.id,is_bot,is_admin,dc_id,have_photo,phone,0,is_premium])      
			added = True
		else:
			added = False

		return added
	else:
		return False


def ScrapeMembersByLetter(voip_index, selected_group, mode, d, tot_recent_users, channel_connect, client):
	stop_deep_search_percentage_status = settings.getSetting('stop_deep_search_percentage_status','scraping_settings')
	stop_deep_search_percentage = settings.getSetting('stop_deep_search_percentage','scraping_settings')
	deep_search_pause = settings.getSetting('deep_search_pause','scraping_settings')
	
	# remove " sec" from deep_search_pause
	deep_search_pause = deep_search_pause[:-4]

	deep_search_vowels = settings.getSetting('deep_search_vowels', 'scraping_settings')
	deep_search_consonant_1 = settings.getSetting('deep_search_consonant_1', 'scraping_settings')
	deep_search_consonant_2 = settings.getSetting('deep_search_consonant_2', 'scraping_settings')
	deep_search_accented = settings.getSetting('deep_search_accented', 'scraping_settings')
	
	deep_search_symbols_1 = settings.getSetting('deep_search_symbols_1', 'scraping_settings')
	deep_search_symbols_2 = settings.getSetting('deep_search_symbols_2', 'scraping_settings')

	deep_search_numbers = settings.getSetting('deep_search_numbers', 'scraping_settings')

	deep_search_emoji_1 = settings.getSetting('deep_search_emoji_1', 'scraping_settings')
	deep_search_emoji_2 = settings.getSetting('deep_search_emoji_2', 'scraping_settings')

	deep_search_russian_1 = settings.getSetting('deep_search_russian_1', 'scraping_settings')
	deep_search_russian_2 = settings.getSetting('deep_search_russian_2', 'scraping_settings')
	deep_search_russian_3 = settings.getSetting('deep_search_russian_3', 'scraping_settings')

	
	vowels = ['a', 'e', 'i', 'o', 'u', 'y'] # 6
	consontant_1 = ['r','l','m','n','s','d','h','k','t','c'] # 10
	consontant_2 = ['p','g','b','f','v','w','j','q','x','z'] # 10
	
	accented = ['ò','à','ù','è','é','ì'] # 6
	
	symbols_1 = ['+','_','-','@','.',',',';',':','!','?','&','*','~'] # 13
	symbols_2 = ['(',')','[',']','{','}','/','\\','|','^','%','$','#','"','\'','`'] # 15

	numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] # 10
	
	#most used emoji for usernames
	emoji_1 = ['😊','🔥','🌟','❤️','🖤','✨','💪','🌈','🌸','🌹'] # 10
	emoji_2 = ['🐱','👑','🍀','🎈','🦄','🎉','🎶'] # 7

	russian_1 = ['ы', 'щ', 'к', 'с', 'м', 'э', 'и', 'я', 'х', 'а'] # 10
	russian_2 = ['ю', 'ж', 'ц', 'ч', 'н', 'г', 'в', 'б', 'ь', 'т'] # 10
	russian_3 = ['ё', 'ф', 'п', 'р', 'о', 'л', 'д', 'з', 'й', 'ш'] # 10 
	

	query = []

	if deep_search_vowels == translations['abilitato_first_cap']:
		query = query + vowels
	if deep_search_consonant_1 == translations['abilitato_first_cap']:
		query = query + consontant_1
	if deep_search_consonant_2 == translations['abilitato_first_cap']:
		query = query + consontant_2
	if deep_search_accented == translations['abilitato_first_cap']:
		query = query + accented
	if deep_search_symbols_1 == translations['abilitato_first_cap']:
		query = query + symbols_1
	if deep_search_symbols_2 == translations['abilitato_first_cap']:
		query = query + symbols_2
	if deep_search_numbers == translations['abilitato_first_cap']:
		query = query + numbers
	if deep_search_emoji_1 == translations['abilitato_first_cap']:
		query = query + emoji_1
	if deep_search_emoji_2 == translations['abilitato_first_cap']:
		query = query + emoji_2
	if deep_search_russian_1 == translations['abilitato_first_cap']:
		query = query + russian_1
	if deep_search_russian_2 == translations['abilitato_first_cap']:
		query = query + russian_2
	if deep_search_russian_3 == translations['abilitato_first_cap']:
		query = query + russian_3
	

	if mode == 'Rewrite':
		method = 'w'
	elif mode == 'Add':
		method = 'a'

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = int(voip_index)-1

	if client != False:
		try:
			target_group_entity = client.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))
			is_target = True
		except Exception as e:
			is_target = False
		
		if is_target == True:
			try:
				activeAnalysis()
				all_admin = client.get_participants(target_group_entity, aggressive=False, filter=ChannelParticipantsAdmins)
				blockAnalysis()
			except:
				all_admin = False

			# Get total number of participants
			total_members = False

			try:
				total_members = client(functions.channels.GetFullChannelRequest(target_group_entity))
				print(" [+] Total participants: " + total_members.full_chat.participants_count)
			except:
				pass

			try:
				print(colors.gr+" "+translations['prelevo_membri'])
				print()

				all_participants = []

				for letter in query:

					try:
						print(colors.cy + " [+] "+translations['fetching_letter']+": "+str(letter))

						now_participants = client.get_participants(target_group_entity, limit=None, search=letter)

						# count all_participants
						all_participants = now_participants + all_participants


						if total_members != False:

							# Remove duplicates based on id
							all_participants_without_duplicate = list({each_user.id: each_user for each_user in all_participants}.values())

							# Check difference
							total_found = len(all_participants_without_duplicate)

							print(" [-] Total members found: ", str(total_found) + colors.wreset)
							print()

							if stop_deep_search_percentage_status == 'Enabled':

								if int(total_found) >= int(total_members.full_chat.participants_count * int(stop_deep_search_percentage) / 100):
									print(" [-] Found "+stop_deep_search_percentage+"% of total members. Exiting the process...")
									break
								else:
									# Calcolo percentuale con 2 decimali dopo la virgola
									percentage_of_found = round(int(total_found) / int(total_members.full_chat.participants_count) * 100, 2)
									print(" [-] Found "+str(percentage_of_found)+"% of total members.")
							else:
								percentage_of_found = round(int(total_found) / int(total_members.full_chat.participants_count) * 100, 2)
								print(" [-] Found "+str(percentage_of_found)+"% of total members...")

						print(" ---------------------------------")
						print()
						
						time.sleep(int(deep_search_pause))

						print()

					except:
						pass

				client.disconnect()

				all_participants = all_participants_without_duplicate


			except Exception as e:
				print(e)
				all_participants = False
		else:
			all_participants = False

		if all_participants != False:

			with open("members/members_temp.csv",method,encoding='UTF-8') as f:
				
				print(colors.gr+" "+translations['attendi'])
				
				writer = csv.writer(f,delimiter=",",lineterminator="\n")
				if method == 'w':
					writer.writerow(['username','user id', 'access hash', 'name', 'group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated', 'is_premium'])
				
				voips = getVoips()

				for user in all_participants:

					found_in_own = False

					for x in voips:
						if x['id'] == str(user.id):
							found_in_own = True

					if found_in_own == False:
						if user.username:
							username = user.username
						else:
							username = ""
						if user.first_name:
							first_name = user.first_name
						else:
							first_name = ""
						if user.last_name:
							last_name = user.last_name
						else:
							last_name = ""
						name = (first_name + ' ' + last_name).strip()

						if user.photo:
							try:
								dc_id = user.photo.dc_id
								have_photo = True
							except:
								dc_id = False
								have_photo = False
						else:
							dc_id = False
							have_photo = False

						if user.bot != False:
							is_bot = True
						else:
							is_bot = False

						if user.phone != None:
							phone = user.phone
						else:
							phone = False
						
						if user.premium == True:
							is_premium = True
						else:
							is_premium = False

						is_admin = False

						if all_admin != False:
							for admin in all_admin:
								if admin.id == user.id:
									is_admin = True

						writer.writerow([username,user.id,user.access_hash,name,selected_group.title,selected_group.id,is_bot,is_admin,dc_id,have_photo,phone,0,is_premium])      
			added = True
		else:
			added = False

		return added
	
	else:
		return False



def ScrapeMethodSelector(voip_index, selected_group, voip_name, scraping_method, mode):

	if mode == 'Rewrite':
		method = 'w'
	elif mode == 'Add':
		method = 'a'

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = int(voip_index)-1

	client = test_connection(cpass['credenziali'+str(voip_index)]['phone'],cpass['credenziali'+str(voip_index)]['apiID'],cpass['credenziali'+str(voip_index)]['hashID'],silent_mode=True)
	
	if client != False:

		channel_connect = client.get_entity(selected_group)
		channel_full_info = client(GetFullChannelRequest(channel=channel_connect))

		try:
			activeAnalysis()
			all_admin = client.get_participants(channel_connect, aggressive=False, filter=ChannelParticipantsAdmins)
			blockAnalysis()
		except:
			all_admin = False

		total = channel_full_info.full_chat.participants_count

		total_recent_request = client(functions.channels.GetParticipantsRequest(
								channel=channel_connect,
								filter=types.ChannelParticipantsRecent(),
								offset=0,
								limit=200,
								hash=0
							))

		total_recent_request_users = total_recent_request.users
		tot_recent_users = int(total_recent_request.count)

		d = tot_recent_users/200

		added = False
		
		if scraping_method == 'method_1':
			result = ScrapeMembers(voip_index, selected_group, mode, d, tot_recent_users, channel_connect, client)
			added = result
			
		elif scraping_method == 'method_2':
			try:
				activeAnalysis()
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=201,
									limit=400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 4%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=401,
									limit=600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 6%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=601,
									limit=800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 8%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=801,
									limit=1000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 10%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1001,
									limit=1200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 12%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1201,
									limit=1400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 14%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1401,
									limit=1600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 16%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1601,
									limit=1800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 18%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1801,
									limit=2000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 20%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2001,
									limit=2200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 22%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2201,
									limit=2400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 24%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2401,
									limit=2600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 26%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2601,
									limit=2800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 28%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2801,
									limit=3000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 30%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3001,
									limit=3200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 32%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3201,
									limit=3400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 34%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3401,
									limit=3600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 36%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3601,
									limit=3800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 38%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3801,
									limit=4000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 40%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4001,
									limit=4200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 42%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4201,
									limit=4400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 44%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4401,
									limit=4600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 46%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4601,
									limit=4800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 48%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4801,
									limit=5000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 50%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5001,
									limit=5200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 52%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5201,
									limit=5400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 54%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5401,
									limit=5600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 56%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5601,
									limit=5800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 58%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5801,
									limit=6000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 60%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6001,
									limit=6200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 62%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6201,
									limit=6400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 64%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6401,
									limit=6600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 66%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6601,
									limit=6800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 68%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6801,
									limit=7000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 70%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7001,
									limit=7200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 72%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7201,
									limit=7400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 74%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7401,
									limit=7600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 76%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7601,
									limit=7800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 78%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7801,
									limit=8000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 80%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8001,
									limit=8200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 82%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8201,
									limit=8400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 84%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8401,
									limit=8600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 86%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8601,
									limit=8800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 88%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8801,
									limit=9000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 90%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9001,
									limit=9200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 92%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9201,
									limit=9400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 94%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9401,
									limit=9600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 96%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9601,
									limit=9800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 98%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9801,
									limit=10000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 100%", end="\r")

				blockAnalysis()

				all_participants = total_recent_request_users
				
				if all_participants != False:
					with open("members/members_temp.csv",method,encoding='UTF-8') as f:

						print(colors.gr+" "+translations['attendi'])

						writer = csv.writer(f,delimiter=",",lineterminator="\n")
						if method == 'w':
							writer.writerow(['username','user id', 'access hash','name','group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated', 'is_premium'])
						
						voips = getVoips()

						for user in all_participants:

							found_in_own = False
							
							for x in voips:
								if x['id'] == str(user.id):
									found_in_own = True

							if found_in_own == False:
								if user.username:
									username = user.username
								else:
									username = ""
								if user.first_name:
									first_name = user.first_name
								else:
									first_name = ""
								if user.last_name:
									last_name = user.last_name
								else:
									last_name = ""
								name = (first_name + ' ' + last_name).strip()

								if user.photo:
									dc_id = user.photo.dc_id
									have_photo = True
								else:
									dc_id = False
									have_photo = False

								if user.bot != False:
									is_bot = True
								else:
									is_bot = False

								if user.phone != None:
									phone = user.phone
								else:
									phone = False
								
								if user.premium == True:
									is_premium = True
								else:
									is_premium = False

								is_admin = False

								if all_admin != False:
									for admin in all_admin:
										if admin.id == user.id:
											is_admin = True

								writer.writerow([username,user.id,user.access_hash,name,selected_group.title,selected_group.id,is_bot,is_admin,dc_id,have_photo,phone,0,is_premium])      
						added = True
				else:
					added = False
			except Exception as e:
				added = False

		elif scraping_method == 'method_3':
			result = ScrapeMembersByLetter(voip_index, selected_group, mode, d, tot_recent_users, channel_connect, client)
			added = result
		
		else:
			added = False

		if added == True:

			try:
				print(" [+] "+translations['rimozione_duplicati'])
				
				# Carica il file CSV in un DataFrame
				df = pd.read_csv('members/members_temp.csv')

				# Se mode è Add, carica il file members.csv in un DataFrame
				if mode == 'Add':
					df_old = pd.read_csv('members/members.csv')
					df = pd.concat([df_old, df], ignore_index=True)

				# Rimuove le righe duplicate in base all'ID utente
				df_cleaned = df.drop_duplicates(subset=['user id'])

				# Salva il DataFrame pulito in un nuovo file CSV
				df_cleaned.to_csv('members/members.csv', index=False)

				# Svuota il file temporaneo e aggiunge solo l'intestazione
				with open("members/members_temp.csv","w",encoding='UTF-8') as f:
					writer = csv.writer(f,delimiter=",",lineterminator="\n")
					writer.writerow(['username','user id', 'access hash', 'name', 'group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated', 'is_premium'])

			
			except Exception as e:
				print(colors.re+" [!] " + translations['errore_sconosciuto'])

			blacklist_status = settings.getSetting('blacklist_status', 'scraping_settings')

			if blacklist_status == translations['abilitato_first_cap']:
				try:
					print(" [+] "+translations['rimozione_completata'])

					if not os.path.exists('members/blacklist.csv'):
						print(colors.re+" [!] "+translations['blacklist_non_trovata']+colors.wreset)
					
					else:
						# Check if the blacklist.csv file is empty
						if os.stat('members/blacklist.csv').st_size == 1:
							print()
							print(colors.wy+" "+translations['blacklist_vuota'])
							print()


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
							
						
						# Check if the members.csv file exists
						if not os.path.exists('members/members.csv'):
							print(colors.re+" [!] "+translations['lista_non_trovata']+colors.wreset)

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

					print(colors.gr+" "+translations['lista_salvata'])
					print()

					
				except:
					print(colors.re+" [!] " + translations['errore_sconosciuto'])

		else:
			print(colors.re+" "+translations['impossibile_scaricare_da_destinazione'])

		client.disconnect()

		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.MembersMenu()
	
