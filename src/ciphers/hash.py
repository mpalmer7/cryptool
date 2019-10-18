import requests
import json
import hashlib

url = "https://isc.sans.edu/tools/reversehash.html"
# r = requests.get(url)
# print(r.json())

# query = "bdc87b9c894da5168059e00ebffb9077" #password1234
# query = "fc5e038d38a57032085441e7fe7010b0" #helloworld
# query = "25f9e794323b453885f5181f1b624d0b" #123456789


def rainbow_table_lookup():
    pass


def decrypt(query, ci):
    yield None


def encrypt(str_inp, key=None):
    byte_inp = str_inp.encode()
    return {"sha1": hash_sha1(byte_inp),
            "sha256": hash_sha256(byte_inp),
            "sha512": hash_sha512(byte_inp),
            "md5": hash_md5(byte_inp)}


def hash_sha1(inp_str):
    return hashlib.sha1(inp_str).hexdigest()


def hash_sha256(inp_str):
    return hashlib.sha256(inp_str).hexdigest()


def hash_sha512(inp_str):
    return hashlib.sha512(inp_str).hexdigest()


def hash_md5(inp_str):
    return hashlib.md5(inp_str).hexdigest()





















'''
import os
import urllib.request
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("bs4 package requirement not found.  Will attempt to install.")
    os.system('pip install bs4')
import re
def duckduckgo_search():
    url = "https://duckduckgo.com/html/?q=" + query
    try:
        page = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print("Hashsearch: urllib error")
    soup = BeautifulSoup(page, 'html.parser')
    #print(soup.prettify())

    # test = soup.find_all('result__snippet')# class_="snippet"
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
                 "hash", "hashtable", "element", "strings", "internet", "string", "reverse", "password", "passwords",
                 "value", "values", "create"]
    for key in dict.keys():
        if len(key) < 6:
            drm.append(key)
        elif dict[key] < 3:
            drm.append(key)
        elif key == query:
            drm.append(key)
        elif key.lower() in blacklist:
            drm.append(key)
    # print(query)
    for k in drm:
        dict.pop(k)
    opt = []
    for key in dict:
        opt.append(key)
    return opt
'''