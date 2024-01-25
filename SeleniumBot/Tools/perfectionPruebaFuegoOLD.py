import time
import re
from itertools import permutations
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from threading import Thread
import traceback
#from Screenshot import Screenshot_clipping
#from PIL import Image

listaCodigos=[]
listaHilos=[]
semana=80
vent=1

def scrap(urlCods):
	sumaBool=False
	restaBool=False
	mayusBool=False
	blockBool=False
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
	page = urlopen(urlCods)
	html = page.read().decode("utf-8")
	for let in numDict.keys():
		let2Num = re.compile(re.escape(let), re.IGNORECASE)
		html = let2Num.sub(numDict.get(let), html)
	instrucciones = re.findall(".*property='twitter:issue:description'", html, re.IGNORECASE)[0]
	pattern2 = ".*s[u|ú]ma((.|\n)*)"
	suma = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(suma!=[]):
		sumaBool=True
	pattern2 = ".*resta((.|\n)*)"
	resta = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(resta!=[]):
		restaBool=True
	pattern2 = "may[u|ú]scula"
	mayus = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(mayus!=[]):
		mayusBool=True
	pattern2 = "bloques de "
	block = re.findall(pattern2, instrucciones, re.IGNORECASE)
	if(block!=[]):
		blockBool=True
	print(f"suma: {sumaBool}")
	print(f"resta: {restaBool}")
	print(f"mayus: {mayusBool}")
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
		separadores=["_", "-", "\.", "\s+", ",", ":", "\*", "\+"]
		for i in range(len(separadores)):
			pattern = "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]"
			m = re.findall(pattern, html)
			if(m==[]):
				pattern = "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" +separadores[i] + "[^ ]"
				m = re.findall(pattern, html)
			if(m!=[]):
				separador=separadores[i]
				break
		if(m==[]):
			for i in range(len(separadores)):
				pattern = "[:>\s][^ ][^ ][^ ]" + separadores[i] + "[^ ][^ ][^ ]" + separadores[i] + "[^ ][^ ][^ ][<\s+]"
				m = re.findall(pattern, html)
				if(m!=[]):
					separador=separadores[i]
					blockBool=True
					break
		for j in range(len(m)):
			if(separador=="\s+" and not blockBool):
				m[j]=m[j].replace(" ", "")
			else:
				m[j]=m[j].replace(separador, "")
	else:
		pattern = "[:>\s][^ ][^ ][^ ]\s+[^ ][^ ][^ ]\s+[^ ][^ ][^ ][<\s+]"
		m = re.findall(pattern, html)
	cods=[]
	if(sumaBool or restaBool):
		caracteresCorrectos = []
		for j in m:
			for k in j:
				print(k)
				try:
					print("tried Int")
					k = int(k)
					k += numSuma
					k = str(k)
					print(k)
				except:
					print(k)
					pass
				caracteresCorrectos.append(k)
			cods.append(''.join(caracteresCorrectos))
			caracteresCorrectos=[]
		cods = list(dict.fromkeys(cods))
	if(mayusBool):
		if(cods!=[]):
			m=cods
		print(cods)
		print(m)
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
			cods.append(''.join(temp))
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
	with open('codigos-en-texto.txt', mode='wt', encoding='utf-8') as myfile:
		myfile.write('\n'.join(cods))

def leer():
	global listaCodigos
	with open("codigos-en-texto.txt") as f:
		lines=f.read().splitlines()
		f.close()
		leerLoop="cods"
		for i in lines:
			listaCodigos.append(lines[lines.index(i)])
		if(not(len(listaCodigos)>0)):
			time.sleep(2)
			leerLoop="nocods"
	return leerLoop

def readfresh():
	global listaCodigos
	global semana
	with open("terminado.txt") as t:
		lines=t.read()
		t.close()
		if(semana!=80):
			refreshLoop="noF"
		else:
			refreshLoop="f"
		if(lines=="f"):
			time.sleep(2)
			refreshLoop="f"
	return refreshLoop

def automatico():
	global semana
	global listaCodigos
	leerLoop="nocods"
	driver_path = "chromedriver.exe"
	brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
	options = webdriver.ChromeOptions()
	options.binary_location = brave_path
	options.add_extension("Buster/busterCaptcha.crx")
	options.add_extension("ultrasurf.crx")
	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
	driver.get('https://forocoches.com/codigo/')
	driver.get('chrome-extension://mpbjkejclgfgadiemmefgebjfooflfhl/src/options/index.html')
	while True:
		if(len(driver.window_handles)>1):
			driver.switch_to.window(driver.window_handles[1])
			driver.close();
			driver.switch_to.window(driver.window_handles[0])
			print("switch")
			break
		time.sleep(0.5)
	while True:
		try:
			driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[2]/div[1]/div/div[1]/div[1]").click()
			driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[2]/div[1]/div/div[2]/ul/li[2]").click()
			driver.find_element(By.XPATH, "//*[@id='undefined__native']").click()
			break
		except:
			pass
	ActionChains(driver).send_keys("AIzaSyCaCDsVgKwDb4j3pWKy9mBbwkB1FRWpEPE").perform()
	driver.get('https://forocoches.com/codigo/')
	while(semana!=0):
		while(leerLoop=="nocods"):
			leerLoop=leer()
		driver.find_element(By.NAME, "codigo").send_keys(listaCodigos[0])
		WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']"))).click()
		driver.switch_to.default_content()
		WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]"))).click()
		()
		time.sleep(10)
		driver.switch_to.default_content()
		try:
			driver.find_element(By.XPATH, "/html/body/center/div/form/div[3]/input").click()
		except:
			pass
		time.sleep(5)
		try:
			driver.save_screenshot(f'code{semana}.png')
		except:
			traceback.print_exc()
			pass
		open('codigos-en-texto.txt', 'w').close()
		listaCodigos=[]
		leerLoop="nocods"
		with open('terminado.txt', 'w') as ter:
			ter.write("f")
			ter.close()
		semana-=1
		driver.get('https://forocoches.com/codigo/')
		time.sleep(0.75)

def autoRefresh():
	global semana
	print(semana)
	refreshLoop="noF"
	with open('terminado.txt', 'w') as ter:
		ter.write("noF")
		ter.close()
	driver_path = "chromedriver.exe"
	brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
	options = webdriver.ChromeOptions()
	options.add_extension("ultrasurf.crx")
	options.binary_location = brave_path
	nav = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
	nav.maximize_window()
	nav.get("https://www.getrevue.co/profile/Forocoches")
	time.sleep(2)
	while True:
		if(len(nav.window_handles)>1):
			nav.switch_to.window(nav.window_handles[1])
			nav.close();
			nav.switch_to.window(nav.window_handles[0])
			print("switch")
			break
		time.sleep(0.5)
	print("for")
	while(semana!=0):
		print(semana)
		while(refreshLoop=="noF"):
			refreshLoop=readfresh()
			print("read")
			time.sleep(0.75)
		nav.get("https://www.getrevue.co/profile/Forocoches")
		try:
			WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "OK")]'))).click()
		except:
			pass
		while True:
			try:
				try:
					WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, f'//h1[contains(text(), "Esta semana en ForoCoches... - Publicación #{semana}")]'))).click()
					print("noticia click")
					break
				except:
					WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="subject" and text()="Esta semana en ForoCoches... - Publicación #{semana}"]'))).click()
					print("noticia click")
					break
			except:
				WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, f'//a[contains(text(), "Show more issues")]'))).click()
				print("show more")
		time.sleep(3)
		urlCods = nav.current_url
		print("scrap")
		scrap(urlCods)

refreshilo = Thread(target=autoRefresh, args=[])
refreshilo.start()


for i in range(vent):
	new_thread = Thread(target=automatico,args=[])
	new_thread.start()
	time.sleep(16)

print("Done")
input()