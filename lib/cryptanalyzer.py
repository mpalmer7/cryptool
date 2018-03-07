#cryptanalyzer

class cipher:
	def __init__(self, name, length, char_types, set_types, grouping, word_count, number_of_sets):
		self.name = name #str
		self.length = length #dict
		self.char_types = char_types #dict
		self.set_types = set_types #dict
		self.grouping = grouping #dict
		self.word_count = word_count #dict
		self.number_of_sets = number_of_sets #int

def helper_get_set_types(ctext, s):
	for c in list(ctext):
		if c in s[0]:
			return True
	return False
			
def get_set_types(ctext):
	sets = [("abcdefghijklmnopqrstuvwxyz", "L_ALPHA"), ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "U_ALPHA"), 
			("1234567890", "NUMERICALS"), ("!@#$%^&*()_+" + "`~{[}]_-+=|\\\"':;?/>.<,", "SYMBOLS"), (" ", "SPACE")]
	characters_in_ctext, total = list(ctext), len(ctext)
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
	
def get_number_of_sets(inp_settypes):
	#Number of Sets:
	#	-Lower Case (letters)
	#	-Upper Case (letters)
	#	-Numbers
	#	-Symbols
	#	-Space
	n = 0
	for key in inp_settypes:
		if inp_settypes[key] != 0.0:
			n += 1
	return n
	
def cryptanalysis(ctext):	#string
	inp_len = str(len(ctext))
	#print("inp_len =", inp_len)
	inp_ctypes = str(len(set(ctext)))
	#print("inp_ctypes =", inp_ctypes)
	inp_settypes = get_set_types(ctext)
	#print("inp_settypes =", inp_settypes)
	inp_numberofsets = get_number_of_sets(inp_settypes)
	#print("inp_numberofsets =", inp_numberofsets)
	inp_grouping = get_character_grouping(ctext.split(" "))
	#print("inp_grouping =", inp_grouping)
	inp_word_count = str(len(ctext.split(" ")))
	#print("inp_word_count =", inp_word_count)
	
	#                name,       length,          char_types, set_types, grouping, word_count, inp_numberofsets)
	binary = cipher("binary", {"other":5}, {"2":20, "3":15, "4":7, "5":5, "other":0}, {"NUMERICALS":10, "SPACE":5, "other":2}, {"8":10,"other":4}, {"other":5}, {"1":7, "2":4, "other":0})
	b64 = cipher("b64", {"other":5}, {"2":2, "3":2, "4":3, "other":5}, {"SYMBOLS":6, "other":5}, {"other":5}, {"1":8, "other":2}, {"1":0, "2":4, "other":6})
	morse = cipher("morse", {"other":5}, {"2":17, "3":14, "other":0}, {"SYMBOLS":10, "other":3}, {"other":5}, {"1":3, "2":3, "3":3, "other":6}, {"1":6, "other":3})
	singlebyteXOR = cipher("singlebyteXOR", {"other":5}, {"2":2, "3":2, "4":2, "5":2, "other":5}, {"SYMBOLS":3, "SPACE":4,"other":5}, {"other":5}, {"other":5}, {"other":5})
	#subtypeciphers includes ceasar, atbash, reversetext, simple substitution
	subtypeciphers = cipher("subtypeciphers", {"other":5}, {"2":2, "3":2, "4":3, "other":6}, {"U_ALPHA":7, "L_ALPHA":7, "SPACE":5, "other":3}, {"other":5}, {"other":5}, {"other":5})
	hashsearch = cipher("hashsearch", {"other":4}, {"other":4}, {"other":4}, {"other":4}, {"1":9, "other":0}, {"1":0, "2":6, "3":6, "other":2})
	#ASCII = cipher("ASCII", None, {}, {}, {}, {})
	
	cipher_list = [binary, b64, morse, singlebyteXOR, subtypeciphers, hashsearch]
	#machine learning? if it gets the correct code add +.01 to the value, otherwise -.01 (or something along those lines...)
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
		#Update score with value of word_count
		if inp_word_count in cp.word_count.keys():
			score = (score + cp.word_count[inp_word_count]) / 2
		else:
			score = (score + cp.word_count["other"]) / 2
		#num of sets
		if inp_numberofsets in cp.word_count.keys():
			score = (score + cp.word_count[inp_word_count]) / 2
		else:
			score = (score + cp.word_count["other"]) / 2
			
			
		
		#additional of indicators
		if cp.name == "b64":
			#b64 will add '=' to make it divisible by 4
			if "=" in ctext[-4:-1]:
				score = (score + 13) / 2
			#b64 is divisible by 4
			if (len(ctext) % 4) == 0:
				score = (score + 8) / 2
			else:
				score = (score + 0) / 2
		

		#subtypeciphers includes caesar, atbash, simplesub
		if cp.name == "subtypeciphers":
			weights["caesar"] = score
			weights["atbash"] = score - 0.5
			weights["reversetext"] = score - 1
			weights["simplesub"] = score - 1.5
		else:
			weights[cp.name] = score
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
	#print(weights)
	#print(sorted(weights, key=weights.get, reverse=True))
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
	return(sorted(weights, key=weights.get, reverse=True))
	
	
#cryptanalysis(input("Enter code: "))