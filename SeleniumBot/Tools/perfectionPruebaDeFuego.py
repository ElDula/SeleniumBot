import os, time, re, requests, traceback
from itertools import permutations
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
#from Screenshot import Screenshot_clipping
#from PIL import Image

listaCodigos=[]
listaHilos=[]
articleIndex=0
maxCheckCount=10
checkCount=0


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
		let2Num = re.compile(re.escape(let), re.IGNORECASE)
		html = let2Num.sub(numDict.get(let), html)

	instrucciones = re.findall('Las invis.*?</p>', html, re.IGNORECASE)[0]

	pattern2 = "n.mero inicial"
	inicial = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(inicial!=[]):
		remSNum=True

	pattern2 = "n.mero final"
	final = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(final!=[]):
		remFNum=True

	pattern2 = "n.mero.*?al.*?al"
	final = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(final!=[]):
		remSNum=True
		remFNum=True

	pattern2 = ".*s[u|ú]ma((.|\n)*)"
	suma = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(suma!=[]):
		sumaBool=True

	pattern2 = ".*resta((.|\n)*)"
	resta = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(resta!=[]):
		restaBool=True

	pattern2 = "min.sculas.*min.sculas.*may.sculas.*may.sculas"
	mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(mayusInverse!=[]):
		pattern2 = "may.sculas.*may.sculas.*min.sculas.*min.sculas"
		mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
	else:
		pattern2 = "min.sculas.*may.sculas.*may.sculas.*min.sculas"
		mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
		print("FUCKFUCKFUCK")
		print(mayusInverse)
		print("FUCKFUCKFUCK")
		if(mayusInverse!=[]):
			mayusIBool=True
		else:
			pattern2 = "may.sculas.*min.sculas.*min.sculas.*may.sculas"
			mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
			if(mayusInverse!=[]):
				mayusIBool=True
			else:
				pattern2 = "may.sculas.*min.sculas y viceversa"
				mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
				if(mayusInverse!=[]):
					mayusIBool=True
				else:
					pattern2 = "min.sculas.*may.sculas y viceversa"
					mayusInverse = re.findall(pattern2, instrucciones, re.IGNORECASE)
					if(mayusInverse!=[]):
						mayusIBool=True

	pattern2 = "la primera"
	FLMayus = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(FLMayus!=[]):
		FLMayusBool=True

	pattern2 = "bloques de "
	block = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(block!=[]):
		blockBool=True

	print(f"quitaNumInicial: {remSNum}")
	print(f"quitaNumFinal: {remFNum}")
	print(f"suma: {sumaBool}")
	print(f"resta: {restaBool}")
	print(f"mayusInverse: {mayusIBool}")
	print(f"block: {blockBool}")

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
		for h in m:
			h=h[:-1]
			print(h)
			cods.append(h)
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
			print("TESTER")
			print(cods)
			print("ENDTESTER")
			m=cods.copy()
			cods=[]
		for i in m:
			print("test")
			temp = list(i)
			print("TESTER")
			print(temp)
			print("ENDTESTER")
			for l in range(len(temp)):
				if temp[l].isalpha():
					if temp[l].isupper():
						temp[l] = temp[l].lower()
					else:
						temp[l]=temp[l].upper()
					print(temp[l])
				if(temp[l]==separador):
					temp[l]=""
					continue
			cods.append(''.join(temp))
	if(FLMayusBool):
		if(cods!=[]):
			m=cods
		for i in m:
			print(i)
			temp = list(i)
			for l in range(len(temp)):
				print(temp[l])
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
		if(not(len(listaCodigos)>0)):
			time.sleep(2)
			leerLoop='nocods'
	return leerLoop

	fileName = 'cod'
	originalTime = os.path.getmtime(fileName)

	while(True):
		if(os.path.getmtime(fileName) > originalTime):
			originalTime = os.path.getmtime(fileName)
		time.sleep(3)

def automaticoPF(index):
	leerLoop='nocods'
	options = webdriver.ChromeOptions()
	options.add_extension('Buster/busterCaptcha.crx')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
	driver.maximize_window()
	driver.get('https://forocoches.com/codigo/')
	driver.get('chrome-extension://mpbjkejclgfgadiemmefgebjfooflfhl/src/options/index.html')
	while True:
		try:
			driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[2]/div[1]/div/div[1]/div[1]").click()
			driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[2]/div[1]/div/div[2]/ul/li[2]").click()
			driver.find_element(By.XPATH, "//*[@id='undefined__native']").click()
			break
		except:
			pass
	ActionChains(driver).send_keys("AIzaSyBHFJFfzPNslnHkG1xriX-16aF8BnlEOpQ").perform()
	driver.get('https://forocoches.com/codigo/')
	while(leerLoop=="nocods"):
		leerLoop=leer()
	driver.find_element(By.NAME, "codigo").send_keys(listaCodigos[index])
	#if(index==len(listaCodigos)):
	#	index=-1
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']"))).click()
	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]"))).click()
	while True:
		try:
			driver.switch_to.default_content()
			driver.find_element(By.XPATH, "/html/body/center/div/form/div[3]/input").click()
			break
		except:
			time.sleep(1)
	try:
		driver.save_screenshot(f'code{index}.png')
	except:
		pass
	driver.quit()

def autoRefreshPF():
	global articleIndex
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
				print('tryclick1')
				nav.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[{articleIndex}]/div/div[1]/div[1]/a').click()
			except:
				print(traceback.print_exc())
				print('tryclick2')
				WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, f'//time.text()=="MIN AGO"'))).click()
				break
		except:
			print('refresh')
			nav.refresh()
		time.sleep(15)
	#WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/article/section/section[1]/div/div/div[2]/table/tbody/tr/td/div/a"))).click()
	time.sleep(5)
	urlCods = nav.current_url
	#time.sleep(3)
	print('scrap')
	scrap(urlCods)
	articleIndex+=2

	fileName = 'codigosFuego.txt'
	originalTime = os.path.getmtime(fileName)

	while(True):
		if(os.path.getmtime(fileName) > originalTime):
			with open(fileName, 'r') as f:
				originalTime = os.path.getmtime(fileName)
		time.sleep(0.1)

refreshilo = Thread(target=autoRefreshPF, args=[])
refreshilo.start()
for i in range(3):
	new_thread = Thread(target=automaticoPF, args=[i])
	new_thread.start()
	listaHilos.append(new_thread)

print('Done')
input()