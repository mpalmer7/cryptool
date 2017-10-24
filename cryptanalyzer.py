#cryptanalyzer

class cipher:
	def __init__(self, name, path, length, char_types, set_types, grouping):
		self.name = name #str
		self.path = path #currently not used
		
		self.length = length #dict
		self.char_types = char_types #dict
		self.set_types = set_types #dict
		self.grouping = grouping #dict

def helper_get_set_types(ctext, s):
	l = list(ctext)
	for c in l:
		if c in s[0]:
			return True
	return False
			
def get_set_types(ctext):
	s_alphabet_lower = ("abcdefghijklmnopqrstuvwxyz", "L_ALPHA")
	s_alphabet_upper = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "U_ALPHA")
	s_numerical = ("1234567890", "NUMERICALS")
	s_symbol = ("!@#$%^&*()_+" + "`~{[}]_-+=|\\\"':;?/>.<,", "SYMBOLS")
	s_space = (" ", "SPACE")
	sets = [s_alphabet_lower, s_alphabet_upper, s_numerical, s_symbol, s_space]

	characters_in_ctext = list(ctext)
	total = len(ctext)
	groupbyset = {"L_ALPHA":0, "U_ALPHA":0, "NUMERICALS":0, "SYMBOLS":0,"SPACE":0}
	#1) Record the total number of characters by each set.
	for s in sets:
		for c in characters_in_ctext:
			if c in s[0]:
				groupbyset[s[1]] += 1
	#2) Change number of characters to % of characters. 
	for gro in groupbyset.keys():
		try:
			gro_weight = (groupbyset[gro] / total)
			groupbyset[gro] = gro_weight
		except ZeroDivisionError:
			groupbyset[gro] = 0
	return groupbyset
	
def get_character_grouping(words):
	gro_total = len(words)
	#1) Get len of each word
	word_sizes = []
	for word in words:
		word_sizes.append(len(word))
	#2) Sort by number of words of each len
	ig = {}
	for n in word_sizes:
		if n in ig.keys():
			ig[n] += 1
		else:
			ig[n] = 1
	#3) Change number to % of words of a len
	for gro in ig.keys():
		gro_weight = (ig[gro] / gro_total)
		ig[gro] = gro_weight
	return ig
	
def cryptanalysis(ctext):	#string
	inp_len = str(len(ctext))
	#print("inp_len =", inp_len)
	inp_ctypes = str(len(set(ctext)))
	#print("inp_ctypes =", inp_ctypes)
	inp_settypes = get_set_types(ctext)
	#print("inp_settypes =", inp_settypes)
	inp_grouping = get_character_grouping(ctext.split(" "))
	#print("inp_grouping =", inp_grouping)
	
	#                 name, path, length, char_types, set_types, grouping)
	binary = cipher("binary", None, {"other":5}, {"2":20, "3":15, "4":7, "5":5, "other":0}, {"NUMERICALS":10, "SPACE":5, "other":2}, {"8":10,"other":4})
	b64 = cipher("b64", None, {"other":5}, {"2":2, "3":2, "4":3, "other":5}, {"SYMBOLS":6, "other":5}, {"other":5})
	morse = cipher("morse", None, {"other":5}, {"2":17, "3":14, "other":0}, {"SYMBOLS":10, "other":3}, {"other":5})
	singlebyteXOR = cipher("singlebyteXOR", None, {"other":5}, {"2":2, "3":2, "4":2, "5":2, "other":5}, {"SYMBOLS":3, "SPACE":4,"other":5}, {"other":5})
	#subtypeciphers includes ceasar, atbash, simple substitution
	subtypeciphers = cipher("subtypeciphers", None, {"other":5}, {"2":2, "3":2, "4":3, "other":6}, {"U_ALPHA":7, "L_ALPHA":7, "SPACE":5, "other":3}, {"other":5})
	hashsearch = cipher("hashsearch", None, {"other":5}, {"other":5}, {"other":5}, {"other":5})
	#ASCII = cipher("ASCII", None, {}, {}, {}, {})
	
	cipher_list = [binary, b64, morse, singlebyteXOR, subtypeciphers, hashsearch]
	#machine learning? if it gets the correct code add +1 to the value, otherwise -1 (or something along those lines...)
	weights = {}
	
	for cp in cipher_list:
		score = 5
		#Update score with value of len
		if inp_len in cp.length.keys():
			score = (score + cp.length[inp_len]) / 2
		else:
			score = (score + cp.length["other"]) / 2	
		#"                     " of character types
		if inp_ctypes in cp.char_types.keys():
			score = (score + cp.char_types[inp_ctypes]) / 2
		else:
			score = (score + cp.char_types["other"]) / 2
		#of set types
		total = 0
		for setn in inp_settypes.keys():
			if str(setn) in cp.set_types.keys():
				total += cp.set_types[setn] * inp_settypes[setn]
			else:
				total += cp.set_types["other"] * inp_settypes[setn]
		score = (score + total) / 2
		#of word grouping
		total = 0
		for gro in inp_grouping.keys():
			if str(gro) in cp.grouping.keys():
				total += cp.grouping[str(gro)] * inp_grouping[gro]
			else:
				total += cp.grouping["other"] * inp_grouping[gro]
		score = (score + total) / 2
		
		#rest of indicators
		if cp.name == "b64":
			if "=" in ctext[-4:-1]:
				score = (score + 13) / 2
			#base 64 is divisible by 4
			if (len(ctext) % 4) == 0:
				score = (score + 8) / 2
			else:
				score = (score + 0) / 2
			#base 64 is a single block of text as an input
			if len(ctext.split(" ")) == 1:
				score = (score + 10) / 2
			else:
				score = (score + 2) / 2
		if cp.name == "hashsearch":
			if len(ctext.split(" ")) == 1:
				score = (score + 10) / 2
			else:
				score = (score + 2) / 2

		
		#subtypeciphers includes caesar, atbash, simplesub
		if cp.name != "subtypeciphers":
			weights[cp.name] = score
		else:
			weights["caesar"] = score
			weights["atbash"] = score - 1
			weights["simplesub"] = score - 2
	
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
	#print(weights)
	#print(sorted(weights, key=weights.get, reverse=True))
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
	return(sorted(weights, key=weights.get, reverse=True))
	
	
#cryptanalysis(input("Enter code: "))