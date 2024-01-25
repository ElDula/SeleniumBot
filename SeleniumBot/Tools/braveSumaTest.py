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
semana=53

def scrap(urlCods):
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
	codeOp = "suma"
	rs2 = 0
	pattern2 = ".*s[u^ú]ma((.|\n)*)"
	m2 = re.findall(pattern2, html, re.IGNORECASE)
	if(m2==[]):
		pattern2 = "may.sculas"
		m2 = re.findall(pattern2, html, re.IGNORECASE)
		codeOp="letters"
		if(m2==[]):
			pattern2 = "bloques de "
			m2 = re.findall(pattern2, html, re.IGNORECASE)
			codeOp = "bloques"
			if(m2==[]):
				pattern2 = "n.mero. ....................................... par.ntesis" 
				m2 = re.findall(pattern2, html, re.IGNORECASE)
				codeOp = "numPar"
	if(codeOp=="suma"):
		texto = m2[0][0]
		for i in texto:
			try:
				i = int(i)
				numSuma=i
				break
			except:
				continue

#		suma = m2[0].split()[0]
#		try:
#			rs2 = int(str(suma[1:]))
#		except Exception as e:
#			rs2 = int(str(suma[:2]))
	if(codeOp!="bloques"):
		separadores=["_", "-", "\.", ",", ":", "\*", "\+", "\s"]
		for i in range(len(separadores)):
			pattern = "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]"
			m = re.findall(pattern, html)
			if(m==[]):
				pattern = "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" + separadores[i] + "[^ ]" +separadores[i] + "[^ ]"
				m = re.findall(pattern, html)
			if(m!=[]):
				separador=separadores[i]
				break
		for j in range(len(m)):
			if(separador=="\s"):
				m[j]=m[j].replace(" ", "")
			else:
				m[j]=m[j].replace(separador, "")
	else:
		pattern = ">...\s+...\s+...\s*<"
		m = re.findall(pattern, html)
	if(m!=[] and codeOp!="bloques" and codeOp!="numPar" and codeOp!="letters"):
		cods=[]
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

#		
#		for codigo in m:
#			correctLet=[]
#			for char in codigo:
#				try:
#					if(char==separador):
#						char=""
#						continue
#					char=str(int(char)+rs2)
#				except Exception as e:
#					pass
#				if(char!=""):
#					correctLet.append(char)
#			cods.append(''.join(correctLet))
		cods = list(dict.fromkeys(cods))
		with open('codigos-en-texto.txt', mode='wt', encoding='utf-8') as myfile:
			myfile.write('\n'.join(cods))
	elif(codeOp=="letters"):
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
		with open('codigos-en-texto.txt', mode='wt', encoding='utf-8') as myfile:
			myfile.write('\n'.join(cods))
	elif(codeOp=="numPar"):
		cods=[]
		actualNums=[0,1,2,3,4,5,6,7,8,9]
		for codigo in m:
			correctLet=[]
			temp=codigo.split()
			for thing in temp:
				if(thing in separador):
					thing=actualNums[separador.index(thing)]
				correctLet.append(thing)
			cods.append(''.join(correctLet))
		cods = list(dict.fromkeys(cods))
		with open('codigos-en-texto.txt', mode='wt', encoding='utf-8') as myfile:
			myfile.write('\n'.join(cods))
	elif(codeOp=="bloques"):
		cods=[]
		for i in m:
			i = i[1:-1]
			temp=i.split()
			lista = list(permutations(temp, 3))
			for j in lista:
				cods.append(''.join(list(j)))
		cods = list(dict.fromkeys(cods))
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

def automatico(i):
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
	while(leerLoop=="nocods"):
		leerLoop=leer()
	driver.find_element(By.NAME, "codigo").send_keys(listaCodigos[i])
	#if(i==len(listaCodigos)):
	#	i=-1
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']"))).click()
	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]"))).click()
	time.sleep(6)
	driver.switch_to.default_content()
	driver.find_element(By.XPATH, "/html/body/center/div/form/div[3]/input").click()
	time.sleep(5)
	try:
		driver.save_screenshot(f'code{semana}.png')
	except:
		pass
	print("done")
	input()

def autoRefresh():
	global semana
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
		if(len(nav.window_handles)==2):
			nav.switch_to.window(nav.window_handles[1])
			nav.close();
			nav.switch_to.window(nav.window_handles[0])
			break
		time.sleep(0.5)
	nav.get("https://www.getrevue.co/profile/Forocoches")
	try:
		WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/a"))).click()
	except:
		pass
	while True:
		try:
			try:
				WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, f'//h1[contains(text(), "Esta semana en ForoCoches... - Publicación #{semana}")]'))).click()
				break
			except:
				WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="subject" and text()="Esta semana en ForoCoches... - Publicación #{semana}"]'))).click()
				break
		except:
			print("refresh")
			nav.refresh()
		time.sleep(15)
	#WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/article/section/section[1]/div/div/div[2]/table/tbody/tr/td/div/a"))).click()
	time.sleep(3)
	urlCods = nav.current_url
	#time.sleep(3)
	print("scrap")
	scrap(urlCods)
	nav.close()

refreshilo = Thread(target=autoRefresh, args=[])
refreshilo.start()

vent=1
for i in range(vent):
	new_thread = Thread(target=automatico,args=[i])
	new_thread.start()
	time.sleep(16)

print("Done")
input()