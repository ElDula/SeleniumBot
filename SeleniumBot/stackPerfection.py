import time
import re
from itertools import permutations
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
import traceback
#from Screenshot import Screenshot_clipping
#from PIL import Image

listaCodigos=[]
listaHilos=[]
ventsTouch=0
ventsTroywell=0
ventsUrban=30#VPN mas estable


def scrap(urlCods):
	remSNum=False
	remFNum=False
	sumaBool=False
	restaBool=False
	mayusIBool=False
	blockBool=False
	FLMayusBool=False
	numDict={
		"(CERO)" : "0",
		"(UNO)" : "1",
		"(DOS)" : "2",
		"(TRES)" : "3",
		"(CUATRO)" : "4",
		"(CINCO)" : "5",
		"(SEIS)" : "6",
		"(SIETE)" : "7",
		"(OCHO)" : "8",
		"(NUEVE)" : "9"
	}
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
	html = requests.get(urlCods, headers=headers).text
	#print(html)
	for let in numDict.keys():
		let2Num = re.compile(re.escape(let), re.IGNORECASE)#Se genera un patrón con las claves del diccionario (mapa) definido antes
		html = let2Num.sub(numDict.get(let), html)#Se sustituye el texto encontrado con el patrón por el valor correspondiente en el diccionario

	instrucciones = re.findall('Las invis.*?</p>', html, re.IGNORECASE)[0]#Se buscan las instrucciones que hay que hacer sobre los códigos

	pattern2 = "n.mero inicial"#"Elimina el NUMERO INICIAL de cada código"
	inicial = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(inicial!=[]):
		remSNum=True

	pattern2 = "n.mero final"#"Elimina el NUMERO FINAL de cada código"
	final = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(final!=[]):
		remFNum=True

	pattern2 = "n.mero.*?al.*?al"#"Elimina el (NUMERO INICIAL y FINAL)/(NUMERO FINAL e INICIAL) de cada código"
	final = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(final!=[]):
		remSNum=True
		remFNum=True

	pattern2 = ".*s[u|ú]ma((.|\n)*)"#Suma X a cada número
	suma = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(suma!=[]):
		sumaBool=True

	pattern2 = ".*resta((.|\n)*)"#Resta X a cada número
	resta = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(resta!=[]):
		restaBool=True

	pattern2 = "min.sculas.*min.sculas.*may.sculas.*may.sculas"#m->m y M->M
	mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(mayusInverse!=[]):
		pattern2 = "may.sculas.*may.sculas.*min.sculas.*min.sculas"#M->M y m->m
		mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
	else:
		pattern2 = "min.sculas.*may.sculas.*may.sculas.*min.sculas"#m->M y M->m
		mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
		if(mayusInverse!=[]):
			mayusIBool=True
		else:
			pattern2 = "may.sculas.*min.sculas.*min.sculas.*may.sculas"#M->m y m->M
			mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
			if(mayusInverse!=[]):
				mayusIBool=True
			else:
				pattern2 = "may.sculas.*min.sculas.*viceversa"#M->m y VICEVERSA
				mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
				if(mayusInverse!=[]):
					mayusIBool=True
				else:
					pattern2 = "min.sculas.*may.sculas.*viceversa"#m->M y VICEVERSA
					mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
					if(mayusInverse!=[]):
						mayusIBool=True

	pattern2 = "la primera"#La primera letra es mayúsculas
	FLMayus = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(FLMayus!=[]):
		FLMayusBool=True

	pattern2 = "bloques de "#Bloques
	block = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(block!=[]):
		blockBool=True

	#INTRUCCIONES A EJECUTAR
	print(f"quitaNumInicial: {remSNum}")
	print(f"quitaNumFinal: {remFNum}")
	print(f"suma: {sumaBool}")
	print(f"resta: {restaBool}")
	print(f"mayusInverse: {mayusIBool}")
	print(f"block: {blockBool}")

	#OPERACIONES DE INTRUCCIONES
	if(sumaBool):
		texto = suma[0][0]
		for i in texto:
			try:
				i = int(i)
				numSuma=i
				print(f"sumador: {numSuma}")
				break
			except:
				continue
	if(restaBool):
		texto = resta[0][0]
		for i in texto:
			try:
				i = int(i)*-1
				numSuma=i
				print(f"sumador: {numSuma}")
				break
			except:
				continue
	if(not block):
		separadores=[r"\.", r"_", r"-", r"\s+", r",", r":", r"\*", r"\+"]
		for i in range(len(separadores)):
			pattern = "<p>.?[^ ]" + separadores[i] + ".*?" + separadores[i] + "[^ ].?</p>"
			m = re.findall(pattern, html)
			if(m!=[]):
				separador=separadores[i]
				print(f"separador: {separador}")
				break
		if(m==[]):
			for i in range(len(separadores)):
				pattern = r"[:>\s][^ ][^ ][^ ]" + separadores[i] + r"[^ ][^ ][^ ]" + separadores[i] + r"[^ ][^ ][^ ][<\s+]"
				m = re.findall(pattern, html)
				if(m!=[]):
					separador=separadores[i]
					blockBool=True
					break
		for j in range(len(m)):
			if(len(separador)==2):
				separador=separador[1]
			if(separador==r"\s+" and not blockBool):
				m[j]=m[j].replace(" ", "")
			else:
				m[j]=m[j].replace(separador, "")
				m[j]=m[j].replace("<p>", "")
				m[j]=m[j].replace("</p>", "")
	else:
		pattern = r"[:>\s][^ ][^ ][^ ]\s+[^ ][^ ][^ ]\s+[^ ][^ ][^ ][<\s+]"
		m = re.findall(pattern, html)
	cods=[]
	if(remSNum):
		if(cods!=[]):
			m=cods
		for h in m:
			h=h[1:]
			print(h)
			cods.append(h)
	if(remFNum):
		if(cods!=[]):
			m=cods
			cods=[]
		#m2=m
		for h in m:
			h=h[:-1]
			print(h)
			cods.append(h)
	#input()
	if(sumaBool or restaBool):
		if(cods!=[]):
			m=cods
		caracteresCorrectos = []
		for j in m:
			for k in j:
				try:
					k = int(k)
					k += numSuma
					k = str(k)
				except:
					pass
				caracteresCorrectos.append(k)
			cods.append(''.join(caracteresCorrectos))
			caracteresCorrectos=[]
		cods = list(dict.fromkeys(cods))
	if(mayusIBool):
		if(cods!=[]):
			m=cods.copy()
			cods=[]
		for i in m:
			temp = list(i)
			for l in range(len(temp)):
				if temp[l].isalpha():
					if temp[l].isupper():
						temp[l] = temp[l].lower()
					else:
						temp[l]=temp[l].upper()
				if(temp[l]==separador):
					temp[l]=""
					continue
			cods.append(''.join(temp))

	if(FLMayusBool):
		if(cods!=[]):
			m=cods
		for i in m:
			temp = list(i)
			for l in range(len(temp)):
				if temp[l].isalpha():
					if temp[l].isupper():
						temp[l] = temp[l].lower()
					else:
						temp[l]=temp[l].upper()
				if(temp[l]==separador):
					temp[l]=""
					continue
		
			primero = temp[0]
			ultimo = temp[-1]

			temp[0] = ultimo
			temp[-1] = primero


	if(blockBool):
		if(cods!=[]):
			m=cods
		for i in m:
			i = i[1:-1]
			temp=i.split()
			lista = list(permutations(temp, 3))
			for j in lista:
				cods.append(''.join(list(j)))
		cods = list(dict.fromkeys(cods))

	if(cods==[]):
		cods=m
		print(cods)

	#Resultados a archivo de texto
	with open('codigos-en-texto.txt', mode='a+', encoding='utf-8') as myfile:
		for rep in range(15):
			myfile.write('\n'.join(cods))
			myfile.write('\n')

def leer():
	global listaCodigos
	with open('codigos-en-texto.txt') as f:
		lines=f.read().splitlines()
		f.close()
		leerLoop='cods'
		for i in lines:
			listaCodigos.append(lines[lines.index(i)])
		if(not(len(listaCodigos)>0)):#Detecta si hay contenido en la lista/archivo
			time.sleep(2)
			leerLoop='nocods'
	return leerLoop

def automatico(index, locationIndex, touchwellurban):
	leerLoop='nocods'
	options = webdriver.ChromeOptions()
	options.add_extension('Buster/busterCaptcha.crx')
	#Se decide la extensión en vase el parametro introducido
	if(touchwellurban==0):
		vpn='VPN/touch.crx'
	elif(touchwellurban==1):
		vpn='VPN/troywell.crx'
	elif(touchwellurban==2):
		vpn='VPN/Urban.crx'
	options.add_extension(vpn)
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
	driver.maximize_window()
	driver.get('https://forocoches.com/codigo/')
	if(touchwellurban==0):#Configuración de TouchVPN
		driver.get('chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html')
		time.sleep(3)
		driver.switch_to.window(driver.window_handles[0])
		driver.get('chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html')
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[1]/div/span'))).click()
		time.sleep(1)
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div/div[4]/div[2]/div[{locationIndex}]'))).click()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[3]/div[3]'))).click()
		time.sleep(4)
	elif(touchwellurban==1):#Configuración de Troywell
		driver.get('chrome-extension://adlpodnneegcnbophopdmhedicjbcgco/popup.html')
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div/div[3]/div[2]'))).click()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[1]/div[3]/div[3]/div[2]'))).click()
		time.sleep(1)

		element = driver.find_element(By.XPATH, f'/html/body/div/div/div[3]/div/div[2]/div[2]/div[{locationIndex}]')
		actions = ActionChains(driver)
		actions.move_to_element(element).perform()
		element.click()

		#element = driver.find_element(By.XPATH, f'/html/body/div/div/div[3]/div/div[2]/div[2]/div[{locationIndexTroywell}]')
		#element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div/div/div[3]/div/div[2]/div[2]/div[{locationIndexTroywell}]')))
		#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div/div[3]/div/div[2]/div[2]/div[{locationIndexTroywell}]'))).click()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div[1]'))).click()
		time.sleep(4)
	elif(touchwellurban==2):#Configuración de UrbanVPN
		driver.get('chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/popup/index.html')
		time.sleep(1)
		driver.switch_to.window(driver.window_handles[0])
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div[2]/div/div/div[2]/button[2]'))).click()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div[2]/div/div[2]/button[2]'))).click()
		time.sleep(1)
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div[2]/div/div[1]/input'))).click()

		element = driver.find_element(By.XPATH, "//*[contains(text(), 'Spain')]")#IPs de España
		actions = ActionChains(driver)
		actions.move_to_element(element).perform()
		element.click()
		time.sleep(4)
	driver.get('chrome-extension://mpbjkejclgfgadiemmefgebjfooflfhl/src/options/index.html')#Configuración de BusterCaptcha
	while True:
		try:
			driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[2]/div[1]/div/div[1]/div[1]").click()
			driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[2]/div[1]/div/div[2]/ul/li[2]").click()
			driver.find_element(By.XPATH, "//*[@id='undefined__native']").click()
			break
		except:
			pass
	ActionChains(driver).send_keys("AIzaSyD040F7deDe3dbDit0tSmcfAPNpBILuiAo").perform()#Clave API de Google Cloud
	driver.get('https://forocoches.com/codigo/')
	time.sleep(5);
	try:
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/label/input'))).click()
	except:
		pass
	while(leerLoop=="nocods"):
		leerLoop=leer()#Se lee el archivo para comprobar si se han publicado y recogido los códigos
	driver.find_element(By.NAME, "codigo").send_keys(listaCodigos[index])
	#if(index==len(listaCodigos)):
	#	index=-1
	
	#Resolución captcha
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']"))).click()
	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]"))).click()
	while True:
		try:
			driver.switch_to.default_content()
			driver.find_element(By.XPATH, "/html/body/center/div/form/div[3]/input").click()#Canjear
			break
		except:
			time.sleep(1)
	try:
		driver.save_screenshot(f'code{index}.png')#Captura de pantalla
	except:
		pass
	input()

def autoRefresh():#Recarga de la página donde se publican los códigos
	driver_path = 'chromedriver.exe'
	options = webdriver.ChromeOptions()
	#options.add_extension('UltraSurf-Security-Privacy-Unblock-VPN.crx')
	nav = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
	nav.maximize_window()
	nav.get('https://forocoches.substack.com/archive')
	#time.sleep(2)
	#while True:
	#	if(len(nav.window_handles)==2):
	#		nav.switch_to.window(nav.window_handles[1])
	#		nav.close();
	#		nav.switch_to.window(nav.window_handles[0])
	#		break
	#	time.sleep(0.5)
	#nav.get('https://forocoches.substack.com/archive')
	try:
		WebDriverWait(nav, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/a'))).click()
	except:
		pass
	while True:
		try:
			try:
				if(nav.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a').text!='La casa de Xokas, propuesta Copa de la Liga, Tente vs Lego...'):#Hay que actualizar el texto a la publicación más reciente
					nav.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a').click()
				else:
					0/0
				break
			except:
				WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, f'//time.text()=="MIN AGO"'))).click()
				break
		except:
			print('refresh')
			nav.refresh()
		time.sleep(13)
	#WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/article/section/section[1]/div/div/div[2]/table/tbody/tr/td/div/a"))).click()
	time.sleep(5)
	urlCods = nav.current_url
	#time.sleep(3)
	print('scrap')
	scrap(urlCods)
	nav.quit()

#def chatGPT():#funcion para usar IA no terminada/implementada
#	driver_path = 'chromedriver.exe'
#	options = webdriver.ChromeOptions()
#	gpt = webdriver.Chrome(options=options)
#	gpt.get('https://chat.openai.com/chat')
#	WebDriverWait(gpt, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[4]/button[1]'))).click()
#	ActionChains(gpt).send_keys('').perform()

refreshilo = Thread(target=autoRefresh, args=[])
refreshilo.start()#Empieza el hilo de busqueda de códigos
time.sleep(2)
locationIndexTouch,locationIndexTroywell, locationIndexUrban=4,6,1
touchwellurban=0
for i in range(ventsTouch):#hilos de TouchVPN
	new_thread = Thread(target=automatico, args=[i, locationIndexTouch, touchwellurban])
	new_thread.start()
	if(locationIndexTouch<9):
		locationIndexTouch+=1
	else:
		locationIndexTouch=4
touchwellurban=1
for i in range(ventsTouch+1,ventsTroywell+ventsTouch+1):#hilos de Troywell
	new_thread = Thread(target=automatico, args=[i, locationIndexTroywell, touchwellurban])
	new_thread.start()
	if(locationIndexTroywell<21):
		locationIndexTroywell+=1
	else:
		locationIndexTroywell=6
	time.sleep(5)
touchwellurban=2
for i in range(ventsTroywell+1,ventsUrban+ventsTroywell+ventsTouch+1):#hilos de UrbanVPN
	new_thread = Thread(target=automatico, args=[i, locationIndexUrban, touchwellurban])
	new_thread.start()
	if(locationIndexUrban<61):
		locationIndexUrban+=1
	else:
		locationIndexUrban=1
	time.sleep(5)

print('Done')
input()