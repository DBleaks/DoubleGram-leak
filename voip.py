import os, sys, time, re, configparser, signal, random, asyncio, settings, banner, shutil, colors, menu
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ApiIdInvalidError, FloodWaitError, UserPrivacyRestrictedError
from telethon.tl.types import InputPeerEmpty, InputPeerChannel
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest, ExportChatInviteRequest
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon import errors
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import PeerUser
from telethon.errors import SessionPasswordNeededError
from prettytable import PrettyTable, ALL
import textwrap

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

colors.getColors()
log = settings.getSetting('log','general_settings')

if log != translations['disabilitato_first_cap'] and log != translations['abilitato_first_cap']:
	log = translations['disabilitato_first_cap']

breaker_analysis = 0
analysis_running = 0

# Funzione per suddividere il testo in righe di max_length caratteri
def wrap_text(text, max_length=60):
    return '\n'.join(textwrap.wrap(text, max_length))

def getVoips():
	voip = []
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	for each_section in cpass.sections():
		z = 0
		account = {}
		for (each_key, each_val) in cpass.items(each_section):
			if z == 0:
				name = each_val
				account['name'] = name
			elif z == 1:
				phone = each_val
				account['phone'] = phone
			elif z == 2:
				apiID =  each_val
				account['apiID'] = apiID
			elif z == 3:
				hashID = each_val
				account['hashID'] = hashID
			elif z == 4:
				ids = each_val
				account['id'] = ids
			elif z == 5:
				access_hash = each_val
				account['access_hash'] = access_hash
			elif z == 6:
				username = each_val
				account['username'] = username
			elif z == 7:
				status = each_val
				account['status'] = status
			else:
				break
			z = z+1

		voip.append(account)

	return voip


def getName(client):
	if client.get_me().last_name == None:
		last_name = ''
	else:
		last_name = client.get_me().last_name

	name = client.get_me().first_name+" "+last_name
	
	return name


def getRestricted(client):
	limited = False
	analyze_account = settings.getSetting('analyze_account','general_settings')

	try:
		client.send_message('@'+analyze_account,message="Restrictions Test")
	except FloodWaitError as e:
		limited = False
	except Exception as e:
		limited = True

	return limited


def getFlood(client):
	flood = False
	analyze_account = settings.getSetting('analyze_account','general_settings')

	try:
		client.send_message('@'+analyze_account,message="Flood Test")

	except errors.FloodWaitError as e:
		flood = True
	except FloodWaitError as e:
		flood = True
	except Exception as e:
		flood = False

	return flood


def getUsername(client):
	username = client.get_me().username

	return username


def getId(client):
	ids = client.get_me().id

	return ids


def getAccessHash(client):
	access_hash = client.get_me().access_hash

	return access_hash


def test_connection(phone,apiID,hashID,silent_mode):
	try:
		client = TelegramClient('sessions/'+phone, apiID, hashID)

	except ApiIdInvalidError:
		client = False
	except Exception as e:
		client = False

	try:
		client.connect()
		if not client.is_user_authorized():
			client.send_code_request(phone)  
			client.sign_in(phone, input(colors.cy+" "+translations['inserisci_codice_ricevuto']+" "+colors.gr))
		else:
			if silent_mode == False:
				print(colors.cy+" "+translations['accesso_eseguito_correttamente'])
				
	except SessionPasswordNeededError:
		# if 2FA is enabled
		password = input(" [+] Insert the 2FA password:")
		client.sign_in(password=password)
	
	except ApiIdInvalidError:
		client = False
	except Exception as e:
		client = False

	return client


def ManageAccountList(write_method):
	if write_method == 0:
		print()
		print(colors.wm+colors.wy+" "+translations['crea_nuova_lista_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_1'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_2'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_3'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_4'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_5'])
		print()
		print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
		print()
		print(colors.cy+"  y |"+colors.wreset+" "+translations['procedi_first_cap'])
		print()
		
		print(colors.cy+" "+translations['digita_scelta_arrow_line'])
		choise = False
		choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
	
	else:
		choise = 'Y'

	if choise == 'Y' or choise == 'y':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		if write_method == 0:

			print()
			print(colors.wm+colors.wy+" "+translations['crea_nuova_lista_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_1'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_2'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_3'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_4'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_5'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
			print()

			original = r'data/config.data'
			target = r'data/backup-config.data'

			shutil.copyfile(original, target)
			method = 'w'
			start = 0
		
		elif write_method == 1:
			method = 'a'
			cpass = configparser.RawConfigParser()
			cpass.read('data/config.data', encoding="UTF-8")
			start = len(cpass.sections())
			print()
			print(colors.wm+colors.wy+" "+translations['aggiungi_account_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_1'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_2'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_3'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
			print()

		print(" "+translations['quanti_account_inserire'])
		print()
		
		print(colors.cy+" "+translations['digita_scelta_arrow_line'])

		try:
			num_voip = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
		except EOFError:
			num_voip = ''
			pass

		if num_voip == 'q' or num_voip == 'Q' or num_voip == '':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			if write_method == 0:
				menu.ManageAccounts()
			else:
				menu.PrincipalMenu()
		try:
			num_voip = int(num_voip)
		except EOFError:
			pass
		
			if num_voip == 0:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				ManageAccountList(write_method)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			ManageAccountList(write_method)

		if write_method == 0:
			i = 0
		elif write_method == 1:
			i = start
			num_voip = num_voip+start

		if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

		while i < num_voip:
			print()
			print(colors.wm+colors.wy+" "+translations['aggiungi_account_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_1'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_2'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_3'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro']+"  ")
			print()
			print(colors.gr+" "+translations['inserisci_dati_account_line'])
			print(colors.gr+" "+translations['inserisci_dati_account_n']+str(i+1))
			print(colors.gr+" "+translations['inserisci_dati_account_line'])
			time.sleep(0.2)

			try:
				phone = input(colors.cy+" "+translations['inserisci_numero_telefono']+" "+colors.gr)
				time.sleep(0.2)
			except EOFError:
				pass

			if phone == 'q' or phone == 'Q' or phone == '':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				if write_method == 0:
					menu.ManageAccounts()
				else:
					menu.PrincipalMenu()
			try:
				apiID = input(colors.cy+" "+translations['inserisci_api_id']+" "+colors.gr)
				time.sleep(0.2)
			except EOFError:
				pass

			if apiID == 'q' or apiID == 'Q' or apiID == '':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				if write_method == 0:
					menu.ManageAccounts()
				else:
					menu.PrincipalMenu()
			try:
				hashID = input(colors.cy+" "+translations['inserisci_hash_id']+" "+colors.gr)
				time.sleep(0.2)
			except EOFError:
				pass

			if hashID == 'q' or hashID == 'Q' or hashID == '':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				if write_method == 0:
					menu.ManageAccounts()
				else:
					menu.PrincipalMenu()

			print(colors.cy+" "+translations['tentativo_connessione'])
			try:
				client = test_connection(phone,apiID,hashID,silent_mode=False)
			except Exception as e:
				break

			if client != False: 
				name = getName(client)
				username = getUsername(client)
				if username == None:
					username = '/'

				credenziali = configparser.RawConfigParser()
				credenziali.add_section('credenziali'+str(i))
				credenziali.set('credenziali'+str(i), 'name', name)
				credenziali.set('credenziali'+str(i), 'phone', phone)
				credenziali.set('credenziali'+str(i), 'apiID', apiID)
				credenziali.set('credenziali'+str(i), 'hashID', hashID)
				credenziali.set('credenziali'+str(i), 'id', client.get_me().id)
				credenziali.set('credenziali'+str(i), 'access_hash', client.get_me().access_hash)
				credenziali.set('credenziali'+str(i), 'username', '@'+username)
				credenziali.set('credenziali'+str(i), 'status', 'Enabled')

				setup = open('data/config.data', method, encoding="utf-8")
				credenziali.write(setup)
				setup.close()

				print()
				print(colors.gr+" "+translations['account_aggiunto_successo'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				
				client.disconnect()

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
			else:
				print()
				print(colors.re+" "+translations['errore_connessione_account'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				break

			i = i+1 

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.PrincipalMenu()

	elif choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		if write_method == 0:
			menu.ManageAccounts()
		else:
			menu.PrincipalMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ManageAccountList(write_method)
		
	
def handler(signum, frame) -> int:
	if analysis_running == 1:
		res = 0
		while res != 'Y' and res != 'y' and res != 'N' and res != 'n':
			print()
			print()
			print(colors.cy+" "+translations['vuoi_interrompere'])
			print(colors.cy+" "+translations['vuoi_interrompere_line'])
			res = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
			print()
		if res == 'y' or res == 'Y':
			global breaker_analysis
			breaker_analysis = True
			if os.name=='nt':
				print()
				print(" [+] "+translations['riavvio_necessario'])
				print(" [+] "+translations['riavvio_necessario_1'])
				print(colors.wreset)
				sys.exit()
			else:
				python = sys.executable
				os.execl(python, python, * sys.argv)

signal.signal(signal.SIGINT, handler)


def blockBreaker():
	global breaker_analysis
	breaker_analysis = 0


def activeAnalysis():
	global analysis_running
	analysis_running = 1


def blockAnalysis():
	global analysis_running
	analysis_running = 0


def ShowServiceMessages(phone=None,apiID=None,hashID=None):

	if phone == None and apiID == None and hashID == None:
		# The user will select an account to use and then the messages from the chat with Telegram will be shown
		voip_index = AccountSelector('read-messages')

		voips = getVoips() 
		i = 0

		if voip_index == 'q' or voip_index == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.ManageAccounts()
		else:
			try:
				voip_index_mem = int(voip_index)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['scelta_non_valida'])
				ShowServiceMessages()

		found = False

		for account in voips:
			if i == (int(voip_index)-1):
				found = True
				break
			i = i + 1

		if found == False:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			ShowServiceMessages()

		else:
			phone = voips[i]['phone']
			apiID = voips[i]['apiID']
			hashID = voips[i]['hashID']
			

	client = test_connection(phone,apiID,hashID,silent_mode=True)
	
	if client != False:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		try:
			messages = client.get_messages(777000, limit=3)

			messages.reverse()

			table = PrettyTable()
			table.field_names = [translations['data'], translations['messaggio']]
			table.align[translations['data']] = "l"
			table.align[translations['messaggio']] = "l"
			table.hrules = ALL

			table.vertical_char = " "

			message_n = len(messages)
			i = 0
	
			for message in messages:
				message_text = message.message or "/"
				message_text_wrapped = wrap_text(message_text)
				message_date = message.date.strftime("%Y-%m-%d %H:%M:%S")

				if i == message_n-1:
					message_date = colors.cy+message_date
					message_text_wrapped = colors.cy+message_text_wrapped


				table.add_row([message_date, message_text_wrapped])

				i = i + 1

			print(table)

			client.disconnect()
		
		except Exception as e:
			print(colors.re+" [!] "+translations['impossibile_recuperare_chat'])
			print()
			menu.continueToPrincipal()
		
		if len(messages) == 0:
			print()
			print(colors.re+" "+translations['nessun_messaggio_servizio'])
			print()
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.continueToPrincipal()

		else:
			# Mostro pulsante aggiorna e indietro
			print()
			print(colors.cy+" 1 | "+colors.wy+translations['aggiorna_messaggi'])
			print()
			print(colors.cy+" "+translations['premi_q_indietro'])
			print()
		
		while True:
			choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)

			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				menu.ManageAccounts()


			elif choise == '1':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				ShowServiceMessages(phone,apiID,hashID)
				break
		
	else:
		print(colors.re+" "+translations['impossibile_questo_account'])
		print()
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
		menu.continueToPrincipal()
	

def AnalyzeAccounts():
	analyze_account = settings.getSetting('analyze_account','general_settings')

	if analyze_account == 'doublegram_owner' or analyze_account == 'doublegram_test_user' or analyze_account == '' or analyze_account == '/':
		print()
		print(colors.wm+colors.wy+" "+translations['errore_test_user']+" "+colors.wreset)
		print()
		menu.continueToPrincipal()
		
	else:
		activeAnalysis()

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		else:
			print()
			print()

		print()
		print(colors.cy+translations['analisi_account_line'])
		print(colors.cy+translations['analisi_account_cap'])
		print(colors.cy+translations['analisi_account_line'])
		print()

		restricted_count = 0
		flood_count = 0
		cant_connect = 0
		voips = getVoips() 
		i = 0

		for account in voips:
			if breaker_analysis == 0:
				print(colors.wm+colors.wy+" - "+account['name']+colors.wreset)

				try:
					client = test_connection(account['phone'],account['apiID'],account['hashID'],silent_mode=True)
				except:
					print(colors.re+" "+translations['impossibile_questo_account'])
					print()
					cant_connect = cant_connect + 1

				is_client = True
				
				try:
					me = client.get_me()
					if me == None:
						is_client = False
				except:
					is_client = False

				if client != False and is_client == True:

					name = getName(client)
					restricted = getRestricted(client)
					flood = getFlood(client)
					username = getUsername(client)
					
					if username == None:
						username = '/'
					else:
						username = '@'+username
					
					ids = getId(client)
					access_hash = getAccessHash(client)
					userfull = client(GetFullUserRequest(client.get_me()))
					
					try:
						bio = userfull.full_user.about
					except:
						bio = ''

					client.disconnect()
					account['name'] = name
					account['id'] = ids
					account['access_hash'] = access_hash
					account['username'] = username

					if restricted == True:
						restricted_txt = colors.re+translations['si_first_cap']
						restricted_count = restricted_count + 1
					else:
						restricted_txt = colors.wy+translations['no_first_cap']

					if flood == True:
						flood_txt = colors.re+translations['si_first_cap']
						flood_count = flood_count + 1
					else:
						flood_txt = colors.wy+translations['no_first_cap']

					if bio == None:
						bio = '/'

					if account['status'] == 'Enabled':
						status_txt = translations['abilitato_first_cap']
					else:
						status_txt = translations['disabilitato_first_cap']
					
					print(colors.cy+" "+translations['nome_completo']+" "+colors.wy+name)
					print(colors.cy+" "+translations['username_first_cap']+": "+colors.wy+username)
					print(colors.cy+" "+translations['telefono']+": "+colors.wy+account['phone'])
					print(colors.cy+" "+translations['stato_doublegram']+": "+colors.wy+status_txt)
					print(colors.cy+" "+translations['biografia']+":")
					print(" "+colors.wy+bio)
					print(colors.cy+" "+translations['limitato']+": "+colors.wy+restricted_txt)
					print(colors.cy+" "+translations['flood']+": "+colors.wy+flood_txt)
					print()
					print("------------------------------")
					print()

				else:
					print(colors.re+" "+translations['impossibile_questo_account'])
					print()
					account['status'] = 'Disabled'
					cant_connect = cant_connect + 1

				i = i + 1

		if breaker_analysis == 0:
			
			print(" "+colors.wm+colors.wy+" "+str(i)+" "+translations['account_totali_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wg+colors.wy+" "+str(i - restricted_count - cant_connect - flood_count)+" "+translations['account_liberi_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wo+colors.wy+" "+str(flood_count)+" "+translations['account_flood_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wr+colors.wy+" "+str(restricted_count)+" "+translations['account_limitati_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wr+colors.wy+" "+str(cant_connect)+" "+translations['account_falliti_cap']+" "+colors.wreset)
			print()

			i = 0
			f = 0
			length = len(voips)
			
			while i < length:
				
				if f == 0:
					method = 'w'
				else:
					method = 'a'	

				accounts = configparser.RawConfigParser()
				
				accounts.add_section('credenziali'+str(i))
			
				accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
				accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
				accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
				accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
				accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
				accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
				accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
				accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
				
				setup = open('data/config.data', method, encoding='utf-8') 
				accounts.write(setup)
				setup.close()
				
				f = f+1
				i = i+1
		else:
			blockBreaker()

		blockAnalysis()

		menu.continueToPrincipal()


def AccountSelector(mode):
	print()
	if mode == 'adding':
		print(colors.wm+colors.wy+" "+translations['inserisci_utenti_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_per_destinazione']+" ")
		print(" "+colors.cy+translations['seleziona_account_per_destinazione_line'])
	elif mode == 'join':
		print(colors.wm+colors.wy+" "+translations['ingresso_in_dest_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['ingresso_in_dest_txt_1'])
		print(" "+colors.wy+translations['ingresso_in_dest_txt_2'])
		print(" "+colors.wy+translations['ingresso_in_dest_txt_3'])
		print()
		print(colors.gr+" "+translations['seleziona_account_per_destinazione']+" ")
		print(" "+colors.cy+translations['seleziona_account_per_destinazione_line'])
	elif mode == 'updatesurname':
		print(colors.wm+colors.wy+" "+translations['modifica_cognome_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_cognome'])
		print(" "+colors.cy+translations['seleziona_account_cognome_line'])
	elif mode == 'updatename':
		print(colors.wm+colors.wy+" "+translations['modifica_nome_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_nome'])
		print(" "+colors.cy+translations['seleziona_account_nome_line'])
	elif mode == 'updatebio':
		print(colors.wm+colors.wy+" "+translations['modifica_bio_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_bio'])
		print(" "+colors.cy+translations['seleziona_account_bio_line'])
	elif mode == 'updateusername':
		print(colors.wm+colors.wy+" "+translations['modifica_username_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_username'])
		print(" "+colors.cy+translations['seleziona_account_username_line'])
	elif mode == 'invite':
		print(colors.wm+colors.wy+" "+translations['invito_account_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['invito_account_cap_txt_1'])
		print(" "+colors.wy+translations['invito_account_cap_txt_2'])
		print(" "+colors.wy+translations['invito_account_cap_txt_3'])
		print(" "+colors.wy+translations['invito_account_cap_txt_4'])
		print(" "+colors.wy+translations['invito_account_cap_txt_5'])
		print(" "+colors.wy+translations['invito_account_cap_txt_6'])
		print(" "+colors.wy+translations['invito_account_cap_txt_7'])
		print()
		print(colors.gr+" "+translations['seleziona_account_invitare'])
		print(" "+colors.cy+translations['seleziona_account_invitare_line'])
	elif mode == 'members':
		print(colors.gr+" "+translations['seleziona_account_prelevare'])
		print(" "+colors.cy+translations['seleziona_account_prelevare_line'])
	elif mode == 'read-messages':
		print(colors.gr+" "+translations['seleziona_account_lettura_messaggi'])
		print(" "+colors.cy+translations['seleziona_account_lettura_line'])
	elif mode == 'members-r':
		print(colors.gr+" "+translations['seleziona_account_prelevare'])
		print(colors.cy+" "+translations['seleziona_account_prelevare_line'])
	elif mode == 'editvoip':
		print(colors.wm+colors.wy+" "+translations['abilita_disabilita_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_ab_dis']+" ")
		print()
		print(colors.cy+translations['ab_dis_line'])
		print("      "+colors.wg+colors.wy+'  '+colors.wreset+ " = "+translations['abilitato_cap']+"    "+colors.wr+colors.wy+'  '+colors.wreset+ " = "+translations['dis_cap'])
		print(" "+colors.cy+translations['ab_dis_line'])
	elif mode == 'deletevoip':
		print(colors.wm+colors.wy+" "+translations['scollega_account_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['scollega_account_cap_txt_1'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_2'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_3'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_4'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_5'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_6'])
		print()
		print(" "+colors.cy+translations['premi_q_indietro'])
		print()
		print(colors.gr+" "+translations['seleziona_account_scollegare'])
		print(" "+colors.cy+translations['seleziona_account_scollegare_line'])
	elif mode == 'setadmin':
		print(colors.wm+colors.wy+" "+translations['rendi_admin_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_per_destinazione'])
		print(" "+colors.cy+translations['seleziona_account_per_destinazione_line'])
	elif mode == 'unsetadmin':
		print(colors.wm+colors.wy+" "+translations['rimuovi_admin_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_per_destinazione'])
		print(" "+colors.cy+translations['seleziona_account_per_destinazione_line'])
	elif mode == 'leave':
		print(colors.wm+colors.wy+" "+translations['uscita_account_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['uscita_account_cap_txt_1'])
		print(" "+colors.wy+translations['uscita_account_cap_txt_2'])
		print()
		print(colors.gr+" "+translations['seleziona_account_lasciare'])
		print(" "+colors.cy+translations['seleziona_da_cui_uscire_line'])

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	i = 1

	n_abilitati = 0
	n_disabilitati = 0	
	
	for each_section in cpass.sections():
		z = 0
		for (each_key, each_val) in cpass.items(each_section):
			if z == 0:
				name = each_val
			elif z == 1:
				apiID =  each_val
			elif z == 2:
				hashID = each_val
			elif z == 7:
				status = each_val
			
			z = z+1

		if mode == 'editvoip':
			if status == 'Enabled':
				n_abilitati = n_abilitati + 1
				status = colors.wg+colors.wy+'  '+colors.wreset
			else:
				n_disabilitati = n_disabilitati + 1
				status = colors.wr+colors.wy+'  '+colors.wreset

			if i < 10:
				print(colors.cy+"  "+str(i) +" | "+status+' '+name)
			else:
				print(colors.cy+" "+str(i) +" | "+status+' '+name)

		else:
			if i < 10:
				print(colors.cy+"  " +str(i) +" | "+colors.wy+name)
			else:
				print(colors.cy+" "+str(i) +" | "+colors.wy+name)

		i = i + 1

	if mode == 'editvoip':
		print()
		print(" "+colors.wg+colors.wy+" "+str(n_abilitati)+" "+translations['account_abilitati_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wr+colors.wy+" "+str(n_disabilitati)+" "+translations['account_disabilitati_cap']+" "+colors.wreset)

	if i == 1 and mode != 'editvoip':
		print()
		print(colors.re+" "+translations['no_account_selezionabile']+colors.wreset)
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	print()
	choise = menu.setChoise()

	return choise


def GroupChannelSelector(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	target_group = 'q'

	try:
		voip_index = int(voip_index)-1
	except:
		return False

	try:
		client = test_connection(cpass['credenziali'+str(voip_index)]['phone'],cpass['credenziali'+str(voip_index)]['apiID'],cpass['credenziali'+str(voip_index)]['hashID'],silent_mode=True)
	except:
		target_group = False
		client = False
	
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
			client.disconnect()
		except Exception as e:
			try:
				client.disconnect()
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				menu.PrincipalMenu()
			return False
		
		k = 0

		for chat in chats:
			try:
				if hasattr(chat, 'access_hash'):
					if chat.access_hash != None:
						groups.append(chat)
						k = k + 1
			except Exception as o:
				continue

		i=0

		if k > 0:
			for group in groups:
				
				if i < 9:
					print(colors.cy + '  ' + str(i+1) + ' |' + ' ' + colors.wy + group.title)
				else:
					print(colors.cy + ' ' + str(i+1) + ' |' + ' ' + colors.wy + group.title)
				
				i = i + 1
		else:
			try:
				client.disconnect()
			except:
				pass
			
			print()
			print(colors.re+" "+translations['nessun_selezionabile'])

		print()
		print(colors.cy+"  q | <- "+translations['torna_indietro']) 
		g_index = menu.setChoise()

		if g_index != 'q' and g_index != 'Q':
			try:
				g_index = int(g_index)-1
				target_group=groups[g_index]
			except:
				target_group = False
		else:
			target_group = 'q'
	else:
		target_group = False
	return target_group


def GroupChannelSelectorAdmin(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	target_group = 'q'

	try:
		voip_index = int(voip_index)-1
	except:
		return False

	try:
		client = test_connection(cpass['credenziali'+str(voip_index)]['phone'],cpass['credenziali'+str(voip_index)]['apiID'],cpass['credenziali'+str(voip_index)]['hashID'],silent_mode=True)
	except:
		target_group = False
		client = False
	
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
			client.disconnect()
		
		except Exception as e:
			try:
				client.disconnect()
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				menu.PrincipalMenu()
			return False
		
		k = 0

		for chat in chats:
			try:
				if hasattr(chat, 'access_hash'):
					if chat.admin_rights != None:
						groups.append(chat)
						k = k + 1
			except Exception as o:
				continue

		i=0

		if k > 0:
			for group in groups:
				
				if i < 9:
					print(colors.cy + '  ' + str(i+1) + ' |' + ' ' + colors.wy + group.title)
				else:
					print(colors.cy + ' ' + str(i+1) + ' |' + ' ' + colors.wy + group.title)
				
				i = i + 1
		else:
			try:
				client.disconnect()
			except:
				pass
			print()
			print(colors.re+" "+translations['nessun_selezionabile'])

		print()
		print(colors.cy+"  q | <- "+translations['torna_indietro']) 
		g_index = menu.setChoise()

		if g_index != 'q' and g_index != 'Q':
			try:

				g_index = int(g_index)-1
				target_group=groups[g_index]
			except:
				target_group = False
		else:
			target_group = 'q'
	else:
		target_group = False
	return target_group


def EditAccount():
	voip_index = AccountSelector('editvoip')
	voips = getVoips() 
	i = 0

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			EditAccount()

	found = False

	for account in voips:
		if i == (int(voip_index)-1):
			found = True
			if account['status'] == 'Enabled':
				account['status'] = 'Disabled'
				status = 'Disabled'
			else:
				account['status'] = 'Enabled'
				status = 'Enabled'

			name = account['name']

		i = i + 1

	if found == False:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		print(colors.re+" "+translations['scelta_non_valida'])
		EditAccount()
	
	i = 0
	f = 0
	length = len(voips)
	
	while i < length:
		if f == 0:
			method = 'w'
		else:
			method = 'a'	

		accounts = configparser.RawConfigParser()
		
		accounts.add_section('credenziali'+str(i))
	 
		accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
		accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
		accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
		accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
		accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
		accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
		accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
		accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
		
		setup = open('data/config.data', method, encoding='utf-8') 
		accounts.write(setup)
		setup.close()
		
		f = f+1
		i = i+1

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

		if status == 'Enabled':
			status_txt = translations['abilitato_lower']
		else:
			status_txt = translations['disabilitato_lower']

		print(colors.gr+" - "+translations['account_first_cap']+" "+name+" "+status_txt+" "+translations['con_successo'])
	EditAccount()


def DeleteAccount():
	voip_index = AccountSelector('deletevoip')
	voips = getVoips() 
	i = 0

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			DeleteAccount()
	
	i = 0
	f = 0
	length = len(voips)
	
	if voip_index_mem < 1 or voip_index_mem > length:
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		print(colors.re+" "+translations['scelta_non_valida'])
		DeleteAccount()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
		print()
		print(colors.wm+colors.wy+" "+translations['scollega_account_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['scollega_account_cap_txt_1'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_2'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_3'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_4'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_5'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_6'])
		print()
		print(" "+colors.cy+translations['premi_q_indietro'])
		print()
		
		voip_index_this = int(voip_index)-1
		
		print(colors.re+" "+translations['sei_sicuro_rimuovere']+" "+voips[voip_index_this]['name']+"?")
		print()
		print(colors.cy+"  y | "+colors.wy+" "+translations['procedi_first_cap'])
		print()		
		print(colors.cy+" "+translations['digita_scelta_arrow_line'])
		
		choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)

		if choise == 'q' or choise == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			DeleteAccount()
		
		elif choise != 'y' and choise != 'Y':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			DeleteAccount()
		
		elif choise == 'y' or choise == 'Y':

			cpass = configparser.RawConfigParser()
			cpass.read('data/config.data', encoding="UTF-8")
			
			voip_index_this = int(voip_index)-1

			client = False

			try:
				client = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
				try:
					client.disconnect()
				except:
					pass
				
			logged_out = False

			if client != False:
				sessions = client(functions.account.GetAuthorizationsRequest()) 
				for session in sessions.authorizations:
					if str(session.api_id) == str(cpass['credenziali'+str(voip_index_this)]['apiID']):
						result = client.log_out()
						logged_out = True

			while i < length:

				if i != (int(voip_index)-1):
					if f == 0:
						method = 'w'
					else:
						method = 'a'

					if (int(voip_index)-1) == 0 and i == 1:
						method = 'w'	

					accounts = configparser.RawConfigParser()
					
					accounts.add_section('credenziali'+str(f))
				 
					accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
					accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
					accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
					accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
					accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
					accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
					accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
					accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
					
					setup = open('data/config.data', method, encoding="UTF-8") 
					accounts.write(setup)
					setup.close()
				
				else:
					if i == 0 and (int(voip_index)-1) == 0:
						accounts = configparser.RawConfigParser()
						setup = open('data/config.data', 'w', encoding="UTF-8") 
						accounts.write(setup)
						setup.close()

					name = voips[i]['name']

				f = f+1
				i = i+1
	
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
				
			print(colors.gr+" [+] "+translations['account_first_cap']+" "+name+" "+translations['eliminato_successo'])
			if logged_out == False:
				print(colors.re+" "+translations['ma_non_sconnesso']+colors.wreset)
			
			DeleteAccount()


def LeaveGroupChannel(voip_index):
	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('leave')
	else:
		is_error = True

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			LeaveGroupChannel(voip_index=None)

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
			LeaveGroupChannel(voip_index=None)

		voips = getVoips()
		length = len(voips)
	
		if voip_index_mem < 1 or voip_index_mem > length:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			InviteInGroup(voip_index=None)

		print()
		print(colors.wm+colors.wy+" "+translations['uscita_account_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_da_cui_uscire'])
		print(" "+colors.cy+translations['seleziona_da_cui_uscire_line_1'])
		group_channel = GroupChannelSelector(voip_index)
		
		if group_channel == 'q' or group_channel == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			LeaveGroupChannel(voip_index=None)
		else:
			if group_channel == False:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				LeaveGroupChannel(voip_index)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			print()
			print(colors.wm+colors.wy+" "+translations['uscita_account_cap']+" "+colors.wreset)
			print()

			voips = getVoips()

			cpass = configparser.RawConfigParser()
			cpass.read('data/config.data', encoding="UTF-8")
			
			voip_index_this = int(voip_index)-1

			try:
				client = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
				client.disconnect()
				LeaveGroupChannel(voip_index=None)

			entity = client.get_entity(group_channel)

			client.disconnect()
			LevaGroupChannelStarter(voips,client,entity)

			print()
			print(colors.cy+" "+translations['invio_continuare_line'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def LevaGroupChannelAction(voips,client,entity,phone,account):
	try:
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		activeAnalysis()
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)		
		print(" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			print(colors.cy+" "+translations['uscita_in_corso'])
			result = await client.delete_dialog(entity.id)
			print(colors.cy+" "+translations['uscita']+" "+colors.gr+translations['completata_first_cap'])
		except:
			print(colors.cy+" "+translations['uscita']+" "+colors.re+translations['fallita_first_cap']+colors.wreset)

		await client.disconnect()

		blockAnalysis()
		
	return True


async def LevaGroupChannelProcess(voips,client,entity):
	for account in voips:
		if account['status'] == 'Enabled':
			client_voip = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])

			phone = account['phone']
			await asyncio.gather(
				LevaGroupChannelAction(voips,client_voip,entity,phone,account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['uscita_di']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])
			
	return True


def LevaGroupChannelStarter(voips,client,entity):
	asyncio.new_event_loop().run_until_complete(LevaGroupChannelProcess(voips,client,entity))


def AutoJoinGroup(voip_index):
	between_autoinvite_pause = settings.getSetting('between_autoinvite_pause','general_settings')
	if between_autoinvite_pause != translations['nessuna_pausa']:
		between_autoinvite_pause = [int(s) for s in re.findall(r'\b\d+\b', between_autoinvite_pause)]
		between_autoinvite_pause_txt = str(','.join(str(i) for i in between_autoinvite_pause))

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('join')
	else:
		is_error = True

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:

		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			AutoJoinGroup(voip_index=None)

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
			AutoJoinGroup(None)

		voips = getVoips()
		length = len(voips)
	
		if voip_index_mem < 1 or voip_index_mem > length:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			AutoJoinGroup(voip_index=None)

		print()
		print(colors.wm+colors.wy+" "+translations['ingresso_auto_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_destinazione_cap'])
		print(" "+colors.cy+translations['line_destinazione_cap'])
		group_channel = GroupChannelSelector(voip_index)
		
		if group_channel == 'q' or group_channel == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			AutoJoinGroup(voip_index=None)
		else:
			if group_channel == False:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				AutoJoinGroup(voip_index)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			print()
			print(colors.wm+colors.wy+" "+translations['ingresso_auto_cap']+" "+colors.wreset)
			print()

			voips = getVoips()

			cpass = configparser.RawConfigParser()
			cpass.read('data/config.data', encoding="UTF-8")
			
			voip_index_this = int(voip_index)-1

			try:
				client = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['impossibile_account_selezionato'])
				AutoJoinGroup(voip_index=None)

			entity = client.get_entity(group_channel)

			client.disconnect()
			JoinGroupStarter(voips,client,between_autoinvite_pause,entity)

			print()
			print(colors.cy+" "+translations['invio_continuare_line'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def JoinGroupAction(voips,client,between_autoinvite_pause,entity,phone,account):
	activeAnalysis()
	try:
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])
		blockAnalysis()

	async with client:
		activeAnalysis()
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)
		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			print(colors.cy+" "+translations['ingresso_in_corso'])
			result = await client(JoinChannelRequest(channel=entity.username))
			print(colors.cy+" [+] "+translations['ingresso_first_cap']+": "+colors.gr+translations['completato_first_cap'])
		except:
			print(colors.cy+" [!] "+translations['ingresso_first_cap']+": "+colors.re+translations['fallito_first_cap'])

		blockAnalysis()
		await client.disconnect()
		
	return True


async def JoinGroupProcess(voips,client,between_autoinvite_pause,entity):
	for account in voips:
		if account['status'] == 'Enabled':
			client_voip = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])

			phone = account['phone']
			await asyncio.gather(
				JoinGroupAction(voips,client_voip,between_autoinvite_pause,entity,phone,account)
			)
			if between_autoinvite_pause != 'Nessuna pausa':
				print(colors.cy+" "+translations['pausa_ingresso_account'])
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
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['ingresso_di']+" "+account['name']+": " +colors.re+translations['annullato_account_disabilitato'])
			
	return True


def JoinGroupStarter(voips,client,between_autoinvite_pause,entity):
	asyncio.new_event_loop().run_until_complete(JoinGroupProcess(voips,client,between_autoinvite_pause,entity))


def InviteInGroup(voip_index):
	between_invite_pause = settings.getSetting('between_invite_pause','general_settings')
	if between_invite_pause != translations['nessuna_pausa']:
		between_invite_pause = [int(s) for s in re.findall(r'\b\d+\b', between_invite_pause)]
		between_invite_pause_txt = str(','.join(str(i) for i in between_invite_pause))

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('invite')
	

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			InviteInGroup(voip_index=None)

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
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			InviteInGroup(None)

		voip_index_login = voip_index - 1

		voips = getVoips()
		length = len(voips)
	
		if voip_index < 1 or voip_index > length:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			InviteInGroup(voip_index=None)

		print()
		print(colors.wm+colors.wy+" "+translations['invito_account_cap']+" "+colors.wreset)
		print(colors.wm+colors.wy+" "+translations['invito_tramite_cap']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_destinazione_cap'])
		print(colors.cy+translations['line_destinazione_cap'])

		try:
			selected_group = GroupChannelSelector(voip_index)
		except Exception as e:
			InviteInGroup(voip_index=None)

		if selected_group == 'q' or selected_group == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			menu.InviteInGroup(voip_index=None)
		else:
			if selected_group == False:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				InviteInGroup(voip_index)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()

			print()
			print(colors.wm+colors.wy+" "+translations['invito_account_cap']+" "+colors.wreset)
			print(colors.wm+colors.wy+" "+translations['invito_tramite_cap']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()

			try:
				client_voip = test_connection(cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'],silent_mode=True)
			except Exception as e:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['scelta_non_valida'])
				InviteInGroup(voip_index=None)

			if client_voip != False:
				if is_error == True:
					print(colors.re+" "+translations['scelta_non_valida'])
				
			voips = getVoips()
			phone = cpass['credenziali'+str(voip_index_login)]['phone']

			if not hasattr(selected_group, 'access_hash'):
				selected_group.access_hash = selected_group.migrated_to.access_hash

			try:
				group_entity_complete =  client_voip.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))

			except Exception as e:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
				client_voip.disconnect()
				InviteInGroup(voip_index)

			try:
				invite = client_voip(ExportChatInviteRequest(group_entity_complete.id))
			except Exception as e:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				invite = False
				print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				client_voip.disconnect()
				InviteInGroup(voip_index)

			client_voip.disconnect()
			

			asyncio.new_event_loop().run_until_complete(InviteInGroupProcess(cpass,voip_index_login,voips,group_entity_complete,between_invite_pause,phone))

		print(colors.cy+" "+translations['invio_continuare_line'])
		
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	menu.ManageAccounts()


async def InviteInGroupProcess(cpass,voip_index_login,voips,group_entity_complete,between_invite_pause,phone):
	client_voip = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'])
	
	try:
		await client_voip.connect()
		if not await client_voip.is_user_authorized():
			return True

	except Exception as e:
		client_voip = False

	if client_voip != False:
		activeAnalysis()
		async with client_voip:
			me = await client_voip.get_me()

			for account in voips:
				if account['status'] == 'Enabled' and account['hashID'] != cpass['credenziali'+str(voip_index_login)]['hashID']:
					print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)

					if me.id != account['id']:

						try:
							user_to_add = await client_voip.get_entity(PeerUser(int(account['id'])))
						except:
							try:
								user_to_add = await client_voip.get_input_entity(account['username'])				
							except:
								user_to_add = False
						
						if user_to_add != False:

							try:
								await client_voip(InviteToChannelRequest(group_entity_complete, [user_to_add]))
								print(colors.cy+" [+] "+translations['invito_di']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
								print()
								
							except UserPrivacyRestrictedError:
								print(colors.cy+" [!] "+translations['invito_di']+" "+account['name']+": "+colors.re+translations['fallito_first_cap'])
								print(colors.re+" "+translations['restizioni_non_permettono_aggiunta'])
								print()
								continue
							except Exception as e:
								print(colors.cy+" [!] "+translations['invito_di']+" "+account['name']+": "+colors.re+translations['fallito_first_cap'])
								print()
								continue

							if between_invite_pause != translations['nessuna_pausa']:
								print(colors.cy+" "+translations['pausa_ingresso_account'])
								print()
								params = []
								i = 0
								for pause_step in between_invite_pause:
									if i == 0:
										params_0 = pause_step
									else:
										params_1 = pause_step
									i = i + 1

								if i == 1:
									time.sleep(params_0)
								else:
									time.sleep(random.randrange(params_0,params_1))
						else:
							print(colors.cy+" [!] "+translations['invito_di']+" "+account['name']+": "+colors.re+translations['fallito_first_cap'])
							print(colors.re+" "+translations['impossibile_trovare_selezionato'])
							print()
				else:
					if account['hashID'] != cpass['credenziali'+str(voip_index_login)]['hashID']:
						print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
						print(colors.cy+" [+] "+translations['invito_di']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])
						print()
		blockAnalysis()

	await client_voip.disconnect()


def OpenStatusPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_ultimo_accesso_cap']+" "+colors.wreset)
	print()
	print(" "+colors.wy+translations['mostra_ultimo_accesso_cap_txt_1'])
	print(" "+colors.wy+translations['mostra_ultimo_accesso_cap_txt_2'])
	print(" "+colors.wy+translations['mostra_ultimo_accesso_cap_txt_3'])
	print(" "+colors.wy+translations['mostra_ultimo_accesso_cap_txt_4'])
	print(" "+colors.wy+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenStatusPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_ultimo_accesso_cap']+" "+colors.wreset)
	print()
	
	OpenStatusPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def OpenStatusPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
				key=types.InputPrivacyKeyStatusTimestamp(),
				rules=[types.InputPrivacyValueAllowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	
	blockAnalysis()

	return True


async def OpenStatusPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenStatusPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True


def OpenStatusPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(OpenStatusPrivacyProcess(voips))


def CloseStatusPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_accesso_cap']+" "+colors.wreset)
	print()
	print(" "+translations['nascondi_accesso_cap_txt_1'])
	print(" "+translations['nascondi_accesso_cap_txt_2'])
	print(" "+translations['nascondi_accesso_cap_txt_3'])
	print(" "+translations['nascondi_accesso_cap_txt_4'])
	print(" "+translations['solo_abilitati'])
	print()

	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseStatusPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_accesso_cap']+" "+colors.wreset)
	print()
	
	CloseStatusPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def CloseStatusPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyStatusTimestamp(),
						rules=[types.InputPrivacyValueDisallowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	
	blockAnalysis()

	return True



async def CloseStatusPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				CloseStatusPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True

def CloseStatusPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(CloseStatusPrivacyProcess(voips))


def OpenChatInvitePrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['permetti_gruppi_cap']+" "+colors.wreset)
	print()
	print(" "+translations['permetti_gruppi_cap_txt_1'])
	print(" "+translations['permetti_gruppi_cap_txt_2'])
	print(" "+translations['permetti_gruppi_cap_txt_3'])
	print(" "+translations['permetti_gruppi_cap_txt_4'])
	print(" "+translations['solo_abilitati'])
	print()

	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenChatInvitePrivacySettings()
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['permetti_gruppi_cap']+" "+colors.wreset)
	print()
	
	OpenChatInvitePrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def OpenChatInvitePrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyChatInvite(),
						rules=[types.InputPrivacyValueAllowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	
	blockAnalysis()

	return True


async def OpenChatInvitePrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenChatInvitePrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True

def OpenChatInvitePrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(OpenChatInvitePrivacyProcess(voips))


def CloseChatInvitePrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['n_permetti_gruppi_cap']+"   "+colors.wreset)
	print()
	print(" "+translations['n_permetti_gruppi_cap_txt_1'])
	print(" "+translations['n_permetti_gruppi_cap_txt_2'])
	print(" "+translations['n_permetti_gruppi_cap_txt_3'])
	print(" "+translations['n_permetti_gruppi_cap_txt_4'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseChatInvitePrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['n_permetti_gruppi_cap']+"   "+colors.wreset)
	print()
	
	CloseChatInvitePrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def CloseChatInvitePrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyChatInvite(),
						rules=[types.InputPrivacyValueDisallowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True



async def CloseChatInvitePrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				CloseChatInvitePrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True

def CloseChatInvitePrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(CloseChatInvitePrivacyProcess(voips))


def OpenPhoneNumberPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_telefono_cap']+"   "+colors.wreset)
	print()
	print(" "+translations['mostra_telefono_cap_txt_1'])
	print(" "+translations['mostra_telefono_cap_txt_2'])
	print(" "+translations['mostra_telefono_cap_txt_3'])
	print(" "+translations['mostra_telefono_cap_txt_4'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenPhoneNumberPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_telefono_cap']+"   "+colors.wreset)
	print()
	
	OpenPhoneNumberPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def OpenPhoneNumberPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyPhoneNumber(),
						rules=[types.InputPrivacyValueAllowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True


async def OpenPhoneNumberPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenPhoneNumberPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])
			

	return True

def OpenPhoneNumberPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(OpenPhoneNumberPrivacyProcess(voips))


def ClosePhoneNumberPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_telefono_cap']+"  "+colors.wreset)
	print()
	print(" "+translations['nascondi_telefono_cap_txt_1'])
	print(" "+translations['nascondi_telefono_cap_txt_2'])
	print(" "+translations['nascondi_telefono_cap_txt_3'])
	print(" "+translations['nascondi_telefono_cap_txt_4'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		ClosePhoneNumberPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_telefono_cap']+"  "+colors.wreset)
	print()
	
	ClosePhoneNumberPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def ClosePhoneNumberPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyPhoneNumber(),
						rules=[types.InputPrivacyValueDisallowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True


async def ClosePhoneNumberPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				ClosePhoneNumberPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True

def ClosePhoneNumberPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(ClosePhoneNumberPrivacyProcess(voips))


def OpenProfilePicturePrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_immagine_cap']+"  "+colors.wreset)
	print()
	print(" "+translations['mostra_immagine_cap_txt_1'])
	print(" "+translations['mostra_immagine_cap_txt_2'])
	print(" "+translations['mostra_immagine_cap_txt_3'])
	print(" "+translations['mostra_immagine_cap_txt_4'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenProfilePicturePrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_immagine_cap']+"  "+colors.wreset)
	print()
	
	OpenProfilePicturePrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def OpenProfilePicturePrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyProfilePhoto(),
						rules=[types.InputPrivacyValueAllowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True


async def OpenProfilePicturePrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenProfilePicturePrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])
			
	return True


def OpenProfilePicturePrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(OpenProfilePicturePrivacyProcess(voips))


def CloseProfilePicturePrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_immagine_cap']+"  "+colors.wreset)
	print()
	print(" "+translations['nascondi_immagine_cap_txt_1'])
	print(" "+translations['nascondi_immagine_cap_txt_2'])
	print(" "+translations['nascondi_immagine_cap_txt_3'])
	print(" "+translations['nascondi_immagine_cap_txt_4'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseProfilePicturePrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_immagine_cap']+"  "+colors.wreset)
	print()
	
	CloseProfilePicturePrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def CloseProfilePicturePrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyProfilePhoto(),
						rules=[types.InputPrivacyValueDisallowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True


async def CloseProfilePicturePrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				CloseProfilePicturePrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True


def CloseProfilePicturePrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(CloseProfilePicturePrivacyProcess(voips))


def OpenForwardLinkPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_messaggi_inoltrati_cap']+"  "+colors.wreset)
	print()
	print(" "+translations['mostra_messaggi_inoltrati_cap_txt_1'])
	print(" "+translations['mostra_messaggi_inoltrati_cap_txt_2'])
	print(" "+translations['mostra_messaggi_inoltrati_cap_txt_3'])
	print(" "+translations['mostra_messaggi_inoltrati_cap_txt_4'])
	print(" "+translations['mostra_messaggi_inoltrati_cap_txt_5'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenForwardLinkPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['mostra_messaggi_inoltrati_cap']+"  "+colors.wreset)
	print()
	
	OpenForwardLinkPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def OpenForwardLinkPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyForwards(),
						rules=[types.InputPrivacyValueAllowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True


async def OpenForwardLinkPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenForwardLinkPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True


def OpenForwardLinkPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(OpenForwardLinkPrivacyProcess(voips))


def CloseForwardLinkPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_inoltrati_cap']+" "+colors.wreset)
	print()
	print(" "+translations['nascondi_inoltrati_cap_txt_1'])
	print(" "+translations['nascondi_inoltrati_cap_txt_2'])
	print(" "+translations['nascondi_inoltrati_cap_txt_3'])
	print(" "+translations['nascondi_inoltrati_cap_txt_4'])
	print(" "+translations['nascondi_inoltrati_cap_txt_5'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseForwardLinkPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['nascondi_inoltrati_cap']+" "+colors.wreset)
	print()
	
	CloseForwardLinkPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def CloseForwardLinkPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyForwards(),
						rules=[types.InputPrivacyValueDisallowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()

	return True


async def CloseForwardLinkPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				CloseForwardLinkPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True


def CloseForwardLinkPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(CloseForwardLinkPrivacyProcess(voips))


def OpenIncomingCallsPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['permetti_chiamate_cap']+" "+colors.wreset)
	print()
	print(" "+translations['permetti_chiamate_cap_txt_1'])
	print(" "+translations['permetti_chiamate_cap_txt_2'])
	print(" "+translations['permetti_chiamate_cap_txt_3'])
	print(" "+translations['permetti_chiamate_cap_txt_4'])
	print(" "+translations['permetti_chiamate_cap_txt_5'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		OpenIncomingCallsPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['permetti_chiamate_cap']+" "+colors.wreset)
	print()
	
	OpenIncomingCallsPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def OpenIncomingCallsPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyPhoneCall(),
						rules=[types.InputPrivacyValueAllowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	blockAnalysis()
	
	return True


async def OpenIncomingCallsPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenIncomingCallsPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])

	return True


def OpenIncomingCallsPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(OpenIncomingCallsPrivacyProcess(voips))


def CloseIncomingCallsPrivacySettings():
	voips = getVoips()
	i = 0

	print()
	print(colors.wm+colors.wy+" "+translations['blocca_chiamate_cap']+" "+colors.wreset)
	print()
	print(" "+translations['blocca_chiamate_cap_txt_1'])
	print(" "+translations['blocca_chiamate_cap_txt_2'])
	print(" "+translations['blocca_chiamate_cap_txt_3'])
	print(" "+translations['blocca_chiamate_cap_txt_4'])
	print(" "+translations['blocca_chiamate_cap_txt_5'])
	print(" "+translations['solo_abilitati'])

	print()
	choise = input(colors.cy+" "+translations['invio_procedere_q_indietro']+" "+colors.gr)

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	elif choise != '':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		CloseIncomingCallsPrivacySettings()

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	print()
	print(colors.wm+colors.wy+" "+translations['blocca_chiamate_cap']+" "+colors.wreset)
	print()
	
	CloseIncomingCallsPrivacyStarter(voips)
	
	print()
	print(colors.cy+" "+translations['invio_continuare_line'])
	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()
	menu.ManageAccounts();


async def CloseIncomingCallsPrivacyAction(voips,phone,account):
	activeAnalysis()
	try:
		client = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])
		await client.connect()
		if not await client.is_user_authorized():
			return True

	except Exception as e:
		print()
		print(colors.re+" "+translations['impossibile_questo_account'])

	async with client:
		this_voip = await client.get_me()
		print()
		print(colors.wm+colors.wy+" "+translations['account_cap']+": "+this_voip.first_name+colors.wreset)

		print(colors.cy+" [+] "+translations['accesso_a']+" "+account['name']+": "+colors.gr+translations['riuscito_first_cap'])
		
		try:
			result = await client(functions.account.SetPrivacyRequest(
						key=types.InputPrivacyKeyPhoneCall(),
						rules=[types.InputPrivacyValueDisallowAll()]
			))
			print(colors.cy+" "+translations['modifica_imp_pri_1']+" "+colors.gr+translations['riuscita_first_cap'])
		except:
			print(colors.cy+" "+translations['modifica_imp_pri_2']+" "+colors.re+translations['fallita_first_cap'])

		await client.disconnect()
	
	blockAnalysis()

	return True


async def CloseIncomingCallsPrivacyProcess(voips):
	for account in voips:
		if account['status'] == 'Enabled':
			await asyncio.gather(
				OpenIncomingCallsPrivacyAction(voips,account['phone'],account)
			)
		else:
			print()
			print(colors.wm+colors.wy+" "+translations['account_cap']+": "+account['name']+colors.wreset)
			print(colors.cy+" "+translations['modifica_imp_pri_3']+" "+account['name']+": " +colors.re+translations['annullata_account_disabilitato'])
			

	return True


def CloseIncomingCallsPrivacyStarter(voips):
	asyncio.new_event_loop().run_until_complete(CloseIncomingCallsPrivacyProcess(voips))


def SetVoipsAsAdmin(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('setadmin')
	else:
		is_error = True

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index = int(voip_index)
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			SetVoipsAsAdmin(voip_index=None)

		voip_index_login = voip_index - 1

		try:
			client_voip = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'])
		except Exception as e:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			SetVoipsAsAdmin(voip_index=None)

		if client_voip != False:
			if is_error == True:
				print(colors.re+" "+translations['scelta_non_valida'])
			
			print()
			print(colors.wm+colors.wy+" "+translations['rendi_admin_cap']+" "+colors.wreset)
			print(colors.wm+colors.wy+" "+translations['rendi_admin_tramite']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()
			print(colors.gr+" "+translations['seleziona_destinazione_cap'])
			print(colors.cy+" "+translations['visualizzati_solo_dest_dove_admin'])
			print(colors.cy+translations['line_solo_dove_admin'])

			try:
				selected_group = GroupChannelSelectorAdmin(voip_index)
			except Exception as e:
				SetVoipsAsAdmin(voip_index=None)

			if selected_group == 'q' or selected_group == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				SetVoipsAsAdmin(voip_index=None)
			else:
				if selected_group == False:

					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					
					SetVoipsAsAdmin(voip_index)

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()

				print()
				print(colors.wm+colors.wy+" "+translations['rendi_admin_cap']+" "+colors.wreset)
				print(colors.wm+colors.wy+" "+translations['rendi_admin_tramite']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
				print()
				voips = getVoips()

				if not hasattr(selected_group, 'access_hash'):
					selected_group.access_hash = selected_group.migrated_to.access_hash

				try:
					client_voip.connect()
					if not  client_voip.is_user_authorized():
						client_voip.send_code_request(cpass['credenziali'+str(voip_index_login)]['phone'])
						client_voip.sign_in(cpass['credenziali'+str(voip_index_login)]['phone'], input(colors.cy+" "+translations['inserisci_codice_ricevuto']+" "+colors.gr))
						client_voip.get_me()

				except Exception as e:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					SetVoipsAsAdmin(voip_index)

				try:
					group_entity_complete = client_voip.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))

				except Exception as e:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()

					print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
					client_voip.disconnect()

					print()
					print(colors.cy+" "+translations['invio_continuare_line'])
					choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

					SetVoipsAsAdmin(voip_index)

				try:
					invite = client_voip(ExportChatInviteRequest(group_entity_complete.id))
				except Exception as e:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					invite = False
					print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
					client_voip.disconnect()

					print()
					print(colors.cy+" "+translations['invio_continuare_line'])
					choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

					SetVoipsAsAdmin(voip_index)

				client_voip.disconnect()
				asyncio.new_event_loop().run_until_complete(SetVoipsAsAdminProcess(cpass,voip_index_login,voips,group_entity_complete))

			print(colors.cy+" "+translations['invio_continuare_line'])
		else:
			print()
			print(colors.re+" "+translations['impossibile_questo_account'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			SetVoipsAsAdmin(voip_index=None)

	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	menu.ManageAccounts()


async def SetVoipsAsAdminProcess(cpass,voip_index_login,voips,group_entity_complete):
	client_voip = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'])
	
	try:
		await client_voip.connect()
		if not await client_voip.is_user_authorized():
			return True

	except Exception as e:
		client_voip = False

	if client_voip != False:
		activeAnalysis()
		async with client_voip:
			me = await client_voip.get_me()

			for account in voips:
				if account['status'] == 'Enabled' and account['hashID'] != cpass['credenziali'+str(voip_index_login)]['hashID']:
					print(colors.cy+" "+translations['provo_a_rendere']+" "+account['name']+" "+translations['admin_dot'])
					
					if me.id != account['id']:
						try:
							user_to_add = await client_voip.get_entity(PeerUser(int(account['id'])))
						except Exception as e:
							try:
								user_to_add = await client_voip.get_input_entity(account['username'])				
							except Exception as i:
								user_to_add = False
						
						if user_to_add != False:
							try:
								await client_voip(functions.channels.EditAdminRequest(
											channel=group_entity_complete,
											user_id=user_to_add,
											admin_rights=types.ChatAdminRights(
												invite_users=True,
												ban_users=True,
											),
											rank=''
										))
								print(colors.cy+" [+] "+account['name']+":"+colors.gr+" "+translations['reso_admin'])
								print()
								
							except UserPrivacyRestrictedError:
								print(colors.cy+" [!] "+colors.re+translations['impossibile_first_cap']+colors.cy+" "+translations['rendere']+" "+account['name']+" "+translations['amministratore_lower'])
								print(colors.re+" "+translations['restizioni_non_permettono_aggiunta'])
								print()
								continue
							except Exception as e:
								#print(e)
								print(colors.cy+" [!] "+colors.re+translations['impossibile_first_cap']+colors.cy+" "+translations['rendere']+" "+account['name']+" "+translations['amministratore_lower'])
								print()
								continue
						else:
							print(colors.cy+" [!] "+colors.re+translations['impossibile_first_cap']+colors.cy+" "+translations['rendere']+" "+account['name']+" "+translations['amministratore_lower'])
							print(colors.re+" "+translations['impossibile_account_selezionato'])
							print()
				else:
					if account['hashID'] != cpass['credenziali'+str(voip_index_login)]['hashID']:
						print(colors.cy+" "+translations['operazione_annullata_per']+": "+account['name']+", "+translations['account_disabilitato'])
						print()
		await client_voip.disconnect()
		blockAnalysis()


def UnsetVoipsAsAdmin(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('unsetadmin')
	else:
		is_error = True

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index = int(voip_index)
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UnsetVoipsAsAdmin(voip_index=None)

		voip_index_login = voip_index - 1

		try:
			client_voip = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'])
		except Exception as e:
			#print(e)
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UnsetVoipsAsAdmin(voip_index=None)

		if client_voip != False:
			if is_error == True:
				print(colors.re+" "+translations['scelta_non_valida'])
			
			print()
			print(colors.wm+colors.wy+" "+translations['rimuovi_admin_cap']+" "+colors.wreset)
			print(colors.wm+colors.wy+" "+translations['rimuovi_admin_tramite']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()
			print(colors.gr+" "+translations['seleziona_destinazione_cap'])
			print(colors.cy+" "+translations['visualizzati_solo_dove_admin'])
			print(colors.cy+translations['line_solo_dove_admin'])

			try:
				selected_group = GroupChannelSelectorAdmin(voip_index)
			except Exception as e:
				UnsetVoipsAsAdmin(voip_index=None)

			if selected_group == 'q' or selected_group == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UnsetVoipsAsAdmin(voip_index=None)
			else:
				if selected_group == False:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					client_voip.disconnect()
					UnsetVoipsAsAdmin(voip_index)

				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()

				print()
				print(colors.wm+colors.wy+" "+translations['rimuovi_admin_cap']+" "+colors.wreset)
				print(colors.wm+colors.wy+" "+translations['rimuovi_admin_tramite']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
				print()

				voips = getVoips()

				if not hasattr(selected_group, 'access_hash'):
					selected_group.access_hash = selected_group.migrated_to.access_hash

				try:
					client_voip.connect()
					if not  client_voip.is_user_authorized():
						client_voip.send_code_request(cpass['credenziali'+str(voip_index_login)]['phone'])
						client_voip.sign_in(cpass['credenziali'+str(voip_index_login)]['phone'], input(colors.cy+" "+translations['inserisci_codice_ricevuto']+" "+colors.gr))
						client_voip.get_me()

				except Exception as e:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					
					UnsetVoipsAsAdmin(voip_index)

				try:
					group_entity_complete = client_voip.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))

				except Exception as e:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
					client_voip.disconnect()
					
					print()
					print(colors.cy+" "+translations['invio_continuare_line'])
					choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
					
					UnsetVoipsAsAdmin(voip_index)

				try:
					invite = client_voip(ExportChatInviteRequest(group_entity_complete.id))
				except Exception as e:
					if log == translations['disabilitato_first_cap']:
						os.system('cls' if os.name=='nt' else 'clear')
						banner.banner()
					invite = False
					print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
					client_voip.disconnect()
					
					print()
					print(colors.cy+" "+translations['invio_continuare_line'])
					choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
					
					UnsetVoipsAsAdmin(voip_index)

				client_voip.disconnect()
				asyncio.new_event_loop().run_until_complete(UnsetVoipsAsAdminProcess(cpass,voip_index_login,voips,group_entity_complete))

			print(colors.cy+translations['invio_continuare_line'])
		else:
			print()
			print(colors.re+" "+translations['impossibile_questo_account'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			UnsetVoipsAsAdmin(voip_index=None)

	choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

	if log == translations['disabilitato_first_cap']:
		os.system('cls' if os.name=='nt' else 'clear')
		banner.banner()

	menu.ManageAccounts()

async def UnsetVoipsAsAdminProcess(cpass,voip_index_login,voips,group_entity_complete):
	client_voip = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'])
	
	try:
		await client_voip.connect()
		if not await client_voip.is_user_authorized():
			return True
		
	except Exception as e:
		client_voip = False

	if client_voip != False:
		activeAnalysis()
		async with client_voip:
			me = await client_voip.get_me()

			for account in voips:
				if account['status'] == 'Enabled' and account['hashID'] != cpass['credenziali'+str(voip_index_login)]['hashID']:
					print(colors.cy+" "+translations['provo_a_rendere']+" "+account['name']+" "+translations['admin_dot'])
					if me.id != account['id']:
						try:
							user_to_add = await client_voip.get_entity(PeerUser(int(account['id'])))
						except Exception as e:
							try:
								user_to_add = await client_voip.get_input_entity(account['username'])				
							except Exception as i:
								user_to_add = False
						
						if user_to_add != False:
							try:
								await client_voip(functions.channels.EditAdminRequest(
										channel=group_entity_complete,
										user_id=user_to_add,
										admin_rights=types.ChatAdminRights(
												invite_users=False,
												ban_users=False,
												),
										rank=''

										))
								print(colors.cy+" [+] "+account['name']+":"+colors.gr+" "+translations['rimosso_come_admin'])
								print()
								
							except UserPrivacyRestrictedError:
								print(colors.cy+" [!] "+colors.re+translations['impossibile_first_cap']+colors.cy+" "+translations['rimuovere']+" "+account['name']+" "+translations['dal_ruolo_admin'])
								print()
								continue
							except Exception as e:
								#print(e)
								print(colors.cy+" [!] "+colors.re+translations['impossibile_first_cap']+colors.cy+" "+translations['rimuovere']+" "+account['name']+" "+translations['dal_ruolo_admin'])
								print()
								continue
						else:
							print(colors.cy+" [!] "+colors.re+"Impossibile"+colors.cy+" "+translations['rimuovere']+" "+account['name']+" "+translations['dal_ruolo_admin'])
							print(colors.re+" "+translations['impossibile_collegarsi_selezionato'])
							print()
				else:
					if account['hashID'] != cpass['credenziali'+str(voip_index_login)]['hashID']:
						print(colors.cy+" "+translations['operazione_annullata_per']+": "+account['name']+", "+translations['account_disabilitato'])
						print()
		await client_voip.disconnect()
		blockAnalysis()


def UpdateUsernameSettings(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('updateusername')
	else:
		is_error = True

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateUsernameSettings(voip_index=None)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		voip_index_login = int(voip_index) - 1

		try:
			client_voip = test_connection(cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'],silent_mode=True)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateUsernameSettings(voip_index=None)

		if client_voip != False:
			if is_error == True:
				print(" "+translations['username_non_disponibile'])

			print()
			print(colors.wm+colors.wy+" "+translations['modifica_username_di']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()
			print(" "+colors.cy+translations['premi_q_indietro'])
			print()
			print(colors.wy+" "+translations['inserisci_username'])
			
			choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateUsernameSettings(voip_index=None)
			try:
				result = client_voip(functions.account.UpdateUsernameRequest(
					username=choise
				))

				voips = getVoips()
				i = 0
				f = 0
				length = len(voips)
				
				while i < length:

					if i == voip_index_login:
						voips[i]['username'] = choise
					
					if f == 0:
						method = 'w'
					else:
						method = 'a'	

					accounts = configparser.RawConfigParser()
					
					accounts.add_section('credenziali'+str(i))
				 
					accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
					accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
					accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
					accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
					accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
					accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
					accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
					accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
					
					setup = open('data/config.data', method, encoding="UTF-8") 
					accounts.write(setup)
					setup.close()
					
					f = f+1
					i = i+1

				print()
				print(colors.gr+" "+translations['modifiche_salvate_successo'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			except Exception as e:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateUsernameSettings(voip_index)

			client_voip.disconnect()
		else:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['impossibile_account_selezionato'])
			UpdateUsernameSettings(voip_index=None)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()


def UpdateNameSettings(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('updatename')
	else:
		is_error = True
	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateNameSettings(voip_index=None)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		voip_index_login = int(voip_index) - 1
		try:
			client_voip = test_connection(cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'],silent_mode=True)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateNameSettings(voip_index=None)

		if client_voip != False:
			if is_error == True:
				print(colors.re+" "+translations['nome_inserito_error'])
				print()

			print()
			print(colors.wm+colors.wy+" "+translations['modifica_nome_di']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()
			print(" "+colors.cy+translations['premi_q_indietro'])
			print()
			
			print(colors.wy+" "+translations['inserisci_nuovo_nome'])
			choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateNameSettings(voip_index=None)
			try:
				result = client_voip(functions.account.UpdateProfileRequest(
					first_name=choise
				))

				voips = getVoips()
				i = 0
				f = 0
				length = len(voips)
				
				while i < length:

					if i == voip_index_login:
						voips[i]['name'] = choise
					
					if f == 0:
						method = 'w'
					else:
						method = 'a'	

					accounts = configparser.RawConfigParser()
					
					accounts.add_section('credenziali'+str(i))
				 
					accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
					accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
					accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
					accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
					accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
					accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
					accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
					accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
					
					setup = open('data/config.data', method, encoding="UTF-8") 
					accounts.write(setup)
					setup.close()
					
					f = f+1
					i = i+1

				print()
				print(colors.gr+" "+translations['modifiche_salvate_successo'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateNameSettings(voip_index)

			client_voip.disconnect()
		
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()


def UpdateSurnameSettings(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('updatesurname')
	else:
		is_error = True
	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateSurnameSettings(voip_index=None)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		voip_index_login = int(voip_index) - 1
		try:
			client_voip = test_connection(cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'],silent_mode=True)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateSurnameSettings(voip_index=None)

		if client_voip != False:
			if is_error == True:
				print(colors.re+" "+translations['cognome_inserito_error'])
				print()

			print()
			print(colors.wm+colors.wy+" "+translations['modifica_cognome_di']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()
			print(" "+colors.cy+translations['premi_q_indietro'])
			print()
			
			print(colors.wy+" "+translations['inserisci_cognome'])
			choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateSurnameSettings(voip_index=None)
			try:
				result = client_voip(functions.account.UpdateProfileRequest(
					last_name=choise
				))

				print()
				print(colors.gr+" "+translations['modifiche_salvate_successo'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateSurnameSettings(voip_index)

			client_voip.disconnect()
		
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()

def UpdateBioSettings(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	is_error = False

	if voip_index == None:
		voip_index = AccountSelector('updatebio')
	else:
		is_error = True
	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateBioSettings(voip_index=None)

		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()

		voip_index_login = int(voip_index) - 1
		try:
			client_voip = test_connection(cpass['credenziali'+str(voip_index_login)]['phone'],cpass['credenziali'+str(voip_index_login)]['apiID'],cpass['credenziali'+str(voip_index_login)]['hashID'],silent_mode=True)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('cls' if os.name=='nt' else 'clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			UpdateBioSettings(voip_index=None)

		if client_voip != False:
			if is_error == True:
				print(colors.re+" "+translations['modifica_bio_error'])
				print()

			print()
			print(colors.wm+colors.wy+" "+translations['modifica_bio_di']+" "+cpass['credenziali'+str(voip_index_login)]['name']+colors.wreset)
			print()
			print(" "+colors.cy+translations['premi_q_indietro'])
			print()
			
			print(colors.wy+" "+translations['inserisci_bio'])
			choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateBioSettings(voip_index=None)
			try:
				result = client_voip(functions.account.UpdateProfileRequest(
					about=choise
				))

				print()
				print(colors.gr+" "+translations['modifiche_salvate_successo'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			except:
				if log == translations['disabilitato_first_cap']:
					os.system('cls' if os.name=='nt' else 'clear')
					banner.banner()
				client_voip.disconnect()
				UpdateBioSettings(voip_index)

			client_voip.disconnect()
		
		if log == translations['disabilitato_first_cap']:
			os.system('cls' if os.name=='nt' else 'clear')
			banner.banner()
		menu.ManageAccounts()

