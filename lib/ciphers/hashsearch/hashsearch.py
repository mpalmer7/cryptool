#md5 reverse hash
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

#query = "bdc87b9c894da5168059e00ebffb9077" #password1234
#query = "fc5e038d38a57032085441e7fe7010b0" #helloworld
#query = "25f9e794323b453885f5181f1b624d0b" #123456789

def decrypt(query, ci):
	url = "https://duckduckgo.com/html/?q="+query
	try:
		page = urllib.request.urlopen(url)
	except urllib.error.HTTPError:
		print("Hashsearch: urllib error")
	soup = BeautifulSoup(page, 'html.parser')
	

	#test = soup.find_all('result__snippet')# class_="snippet"
	test = soup.find_all("a", class_="result__snippet")
	
	new = []
	for t in test:
		new.append(t.text.split(' '))
	dict = {}
	for n in new:
		for phrase in n:
			if query in phrase:
				phrase = re.sub(query, '', phrase)
			try:
				if phrase[0] in ",;:.":
					phrase = phrase[1:]
			except IndexError:
				pass
			try:
				if phrase[-1] in ",;:.":
					phrase = phrase[:-1]
			except IndexError:
				pass
			if phrase in dict.keys():
				dict[phrase] += 1
			else:
				dict[phrase] = 1
	drm = []
	blacklist = ["function", "cracking", "hashing", "decrypt", "download", "pattern", "encrypted", 
				 "through", "development", "devices", "developer", "working", "service", "automatically", 
				 "anagrhash", "pastebin", "security", "professional", "produce", "publish", "recover", 
				 "professionals", "digital", "original", "newspapers", "newspaper", "publications", "magazines", 
				 "hash", "hashtable", "element", "strings", "internet"]
	for key in dict.keys():
		if len(key) < 7:
			drm.append(key)
		elif dict[key] == 1:
			drm.append(key)
		elif key == query:
			drm.append(key)
		elif key.lower() in blacklist:
			drm.append(key)
	for k in drm:
		dict.pop(k)
	opt = []
	for key in dict:
		opt.append(key)
	return opt