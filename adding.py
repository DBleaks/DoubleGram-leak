import os, csv, re, time, configparser, random, asyncio, banner, adder, colors, menu, settings
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChatBannedRights
from datetime import timedelta
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, ChannelParticipantsBanned, ChannelParticipantsKicked
from telethon.tl.functions.channels import InviteToChannelRequest, EditBannedRequest
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError
from telethon.tl.functions.messages import ExportChatInviteRequest
from voip import AccountSelector, GroupChannelSelector, test_connection, getVoips, blockAnalysis

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
	
def AddUsers(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	u  = 0

	with open(r"members/members.csv", encoding='UTF-8') as f:  
		rows = csv.reader(f,delimiter=",",lineterminator="\n")
		next(rows, None)
		for row in rows:
			u = u + 1

	if u > 0:
		is_error = False

		if voip_index == None:
			voip_index = AccountSelector('adding')
		else:
			is_error = True

		if voip_index == 'q' or voip_index == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.AddingMenu()
		else:

			try:
				voip_index_mem = int(voip_index)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" [!] Scelta non valida")
				AddUsers(voip_index=None)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			if is_error == True:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print()
				print(colors.re+" "+translations['impossibile_questo_account'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				AddUsers(None)

			print()
			print(colors.wm+colors.wy+" "+translations['inserisci_utenti_cap']+" "+colors.wreset)
			print()
			print(colors.gr+" "+translations['seleziona_destinazione_cap']+" ")
			print(colors.cy+translations['line_destinazione_cap'])
			selected_group = GroupChannelSelector(voip_index)
			
			if selected_group == 'q' or selected_group == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				AddUsers(voip_index=None)
			else:
				if selected_group == False:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					AddUsers(voip_index)

				voips = getVoips()
				voip_index_this = int(voip_index)-1

				try:
					client_voip = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
				except:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					print(colors.re+" "+translations['impossibile_collegarsi_selezionato'])
					AddUsers(voip_index=None)

				if not hasattr(selected_group, 'access_hash'):
					selected_group.access_hash = selected_group.migrated_to.access_hash

				try:
					group_entity_complete =  client_voip.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))

				except:
					print(colors.re+" "+translations['non_possibile_collegarsi_destinazione'])
					client_voip.disconnect()
					menu.PrincipalMenu()

				try:
					invite = client_voip(ExportChatInviteRequest(group_entity_complete.id))
				except:
					invite = False

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
					
				auto_add_at_start = settings.getSetting('auto_add_at_start','adding_settings')
				
				between_autoinvite_pause = settings.getSetting('between_autoinvite_pause','adding_settings')
				if between_autoinvite_pause != 'Nessuna pausa':
					between_autoinvite_pause = [int(s) for s in re.findall(r'\b\d+\b', between_autoinvite_pause)]
					between_autoinvite_pause_txt = str(','.join(str(i) for i in between_autoinvite_pause))

				if auto_add_at_start == translations['abilitato_first_cap']:

					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()

					print()
					print(colors.gr+" "+translations['invito_account_in_corso'])
					
					for account in voips:
						if client_voip.get_me().id != account['id'] and account['status'] == 'Enabled':
							
							try:
								user_to_add = client_voip.get_input_entity(account['username'])
							except:
								user_to_add = False
							
							if user_to_add != False:

								try:
									client_voip(InviteToChannelRequest(group_entity_complete, [user_to_add]))
									print(colors.gr+" [+] "+account['name']," "+translations['invitato_successo']+colors.wreset)
								
								except UserPrivacyRestrictedError:
									print(colors.re+" "+translations['restizioni_non_permettono_aggiunta']+colors.wreset)
								
								except Exception as e:
									print(colors.re+" "+translations['impossibile_aggiungere_account_destinazione'])
									print(colors.re+"     "+translations['potrebbe_bannato_o_restrizioni']+colors.wreset)
							
							else:
								print(colors.re+" "+translations['impossibile_aggiungere_account_destinazione'])
								print(colors.re+"     "+translations['potrebbe_bannato_o_restrizioni']+colors.wreset)
						
						else:
							print(colors.cy+" [+] "+translations['invito_di']+" "+account['name']+colors.re+" "+translations['annullato_account_disabilitato']+colors.wreset)

						if between_autoinvite_pause != 'Nessuna pausa':
							
							print(" "+translations['pausa_invito_account'])
							print()

							params = []
							i = 0
							
							for pause_step in between_autoinvite_pause:
								if i == 0:
									params_0 = pause_step
								else:
									params_1 = pause_step
								i = i + 1

							if i == 1:
								time.sleep(params_0)
							else:
								time.sleep(random.randrange(params_0,params_1))
				
				print(" [+] "+translations['recupero_presenti'])
				is_error_participants = False

				try:
					all_participants = client_voip.get_participants(selected_group, aggressive=False)
				except:

					print(" [+] "+translations['recupero_presenti_1'])
					is_error_participants = True
					all_participants = False

				try:
					all_kicked = client_voip.get_participants(selected_group, aggressive=False, filter=ChannelParticipantsKicked)
				except:
					print(" [+] "+translations['recupero_presenti_2'])
					is_error_participants = True
					all_kicked = False

				try:
					all_banned = client_voip.get_participants(selected_group, aggressive=False, filter=ChannelParticipantsBanned)
				except:
					print(" [+] "+translations['recupero_presenti_3'])
					is_error_participants = True
					all_banned = False


				if is_error_participants == True:
					print(" [+] "+translations['recupero_presenti_final'])

				client_voip.disconnect()

				adder.startAdder(voips,selected_group,group_entity_complete,invite,all_participants,all_kicked,all_banned)

				blockAnalysis()

				print()
				print(colors.cy+" "+translations['operazione_adding_conclusa'])
				print(colors.cy+" "+translations['line_op_adding_conclusa'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				menu.AddingMenu()
			
	else:
		print()
		print(colors.re+" "+translations['lista_membri_vuota']+"\n "+translations['preleva_membri_per_aggiungerli'])
		print(colors.cy+" "+translations['line_op_adding_conclusa'])
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.AddingMenu()


def RemoveLastAddedUsers():
	users = []
	users_to_remove = []
	num_users = 0
	target = False
	
	with open(r"members/last_added.csv", encoding='UTF-8') as f:  
		rows = csv.reader(f,delimiter=",",lineterminator="\n")
		next(rows, None)
		for row in rows:
			num_users = num_users + 1
			user = {}
			user['username'] = row[0]
			user['id'] = int(row[1])
			user['access_hash'] = int(row[2])
			user['target'] = row[3]
			user['group_id'] = row[4]
			user['access_hash'] = row[5]
			target_id = row[4]
			target = row[5]
			title = row[6]
			users_to_remove.append(user)

		print()
		print(colors.wm+colors.wy+" "+translations['rimuovi_utenti_aggiunti_cap']+colors.wreset)
		print()
		print("  "+colors.wm+colors.wy+translations['numero_inseriti']+" "+str(num_users)+colors.wreset)
		print()
		print("  "+colors.wm+colors.wy+translations['gruppo_destinazione']+" "+str(title)+colors.wreset)
		print()
		print(colors.cy+" "+translations['visualizzati_solo_dove_admin'])
		print(colors.cy+"     "+translations['visualizzati_solo_dove_admin_end'])
		print(colors.cy+translations['line_solo_dove_admin'])	

		voips = getVoips()
		i = 1
		z = 0
		
		for account in voips:
			client = test_connection(account['phone'],account['apiID'],account['hashID'],silent_mode=True)

			if client != False:

				chats = []
				last_date = None
				chunk_size = 200
				groups=[]

				try: 
					result = client(GetDialogsRequest(
							offset_date=last_date,
							offset_id=0,
							offset_peer=InputPeerEmpty(),
							limit=chunk_size,
							hash = 0
					         ))
					chats.extend(result.chats)
				
				except:
					client.disconnect()
					return False

				is_admin = False
				for chat in chats:
					try:
						if chat.admin_rights != None and str(chat.id) == str(target_id):
							is_admin = True
							if i < 10:
								print(colors.cy+'  '+str(i)+' |' + colors.wy+' ' + account['name'])
							else:
								print(colors.cy+' '+str(i)+' |' + colors.wy+' ' + account['name'])
							i = i+1
					except:
						continue

				if is_admin == True:
					users.append(z)
				 
				client.disconnect()
				z = z +1

		if i == 1:
			print()
			print(colors.re+" "+translations['nessun_account_admin_di']+" "+title)
		
		print()
		print(colors.cy+ " q | <- "+translations['torna_indietro'])
		
		
		g_index = menu.setChoise()			
		
		if g_index == 'q' or g_index == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.AddingMenu()

		else:
			try:
				int(g_index)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['scelta_non_valida'])
				RemoveLastAddedUsers()
			k = 1
			
			for user in users:
				if k == int(g_index):
					cpass = configparser.RawConfigParser()
					cpass.read('data/config.data', encoding="UTF-8")
					
					voip_index_this = user

					client = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
					entity = client.get_entity(InputPeerChannel(int(target_id), int(target)))

					all_members = client.get_participants(entity)
					client.disconnect()
					break
			
			asyncio.new_event_loop().run_until_complete(RemoveLastAddedProcess(cpass,voip_index_this,entity,users_to_remove))
			
			with open("members/last_added.csv",'w',encoding='UTF-8') as f:
				writer = csv.writer(f,delimiter=",",lineterminator="\n")
				writer.writerow(['username','user id', 'access hash', 'target_group_entity', 'group_id', 'access_hash'])
					
				k = k+1
	print()
	print(colors.cy+" "+translations['operazione_conclusa'])
	print(colors.cy+" "+translations['line_op_adding_conclusa'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.AddingMenu()


async def RemoveLastAddedProcess(cpass,voip_index_this,entity,users_to_remove):
	client_voip = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'])
	phone = cpass['credenziali'+str(voip_index_this)]['phone']
	try:
		await client_voip.connect()
		if not await client_voip.is_user_authorized():
			await client_voip.send_code_request(phone)
			await client_voip.sign_in(phone, input(colors.cy+' '+translations['inserisci_codice_ricevuto']+' '+colors.gr))
			await client_voip.get_me()

	except Exception as e:
		client_voip = False

	if client_voip != False:
		async with client_voip:
			for user_to_remove in users_to_remove:
				user = await client_voip.get_entity(user_to_remove['id'])
				
				rights = ChatBannedRights(
					until_date=timedelta(days=366),
					view_messages=True,
					send_messages=True,
					send_media=True,
					send_stickers=True,
					send_gifs=True,
					send_games=True,
					send_inline=True,
					embed_links=True
				)

				await client_voip(EditBannedRequest(entity, user, rights))
				print()
				print(colors.wy+" "+translations['utente_arrow']+" -> "+str(user_to_remove['id'])+' rimosso')
			await client_voip.disconnect()
	return