#md5 reverse hash
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

#query = "bdc87b9c894da5168059e00ebffb9077" #password1234
#query = "fc5e038d38a57032085441e7fe7010b0" #helloworld
#query = "d8578edf8458ce06fbc5bb76a58c5ca4" #qwerty
#query = "25f9e794323b453885f5181f1b624d0b" #123456789

def decrypt(query, ci):
	url = "https://www.bing.com/search?q="+query+"&qs=n&form=QBRE&sp=-1&pq="+query
	#print(url)
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	#print(soup.prettify())

	test = soup.find_all('p')# class_="snippet"
	new = []
	for t in test:
		new.append(t.text.split(' '))
	dict = {}
	for n in new:
		for phrase in n:
			if query in phrase:
				print(phrase)
				phrase = re.sub(query, '', phrase)
				print(phrase)
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
	blacklist = ["guess", "value", "pastebin", "crack", "through", "creating", "function", "development", "service", "hash", 
				 "hashes", "python", "encryption", "accept", "decrypt", "reverse", "repair", "product"]
	for key in dict.keys():
		if len(key) < 6:
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