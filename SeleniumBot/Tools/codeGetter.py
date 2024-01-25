import requests
import re
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
	print(html)
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
		for h in m:
			print(h)
			h=h[1:]
			print(h)
			cods.append(h)
	if(remFNum):
		for h in m:
			print(h)
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
				print("puta")
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

		print(temp)


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

	with open('codeGot.txt', mode='a+', encoding='utf-8') as myfile:
		for rep in range(15):
			myfile.write('\n'.join(cods))
			myfile.write('\n')

scrap('https://forocoches.substack.com/p/14-anos-sin-andres-montes-filtran')