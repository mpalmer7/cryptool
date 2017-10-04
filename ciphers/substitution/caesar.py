#Ceasar Key Decryption

aall_comboshabet = "abcdefghijklmnopqrstuvwxyz"
aall_comboshanum = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
			'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16,
			'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
			'y': 25, 'z': 26, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
			'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16,
			'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
			'Y': 25, 'Z': 26}
numaall_combosha = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l',
			13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v',
			23: 'w', 24: 'x', 25: 'y', 26: 'z'}
			
def list_to_string(ls):
	str = ''
	for char in ls:
		str += char
	return str
			
			
def encrypt(plaintext):
		
	key = int(input("Enter integer to rotate by: "))
	for l in range(len(plaintext)):
		plaintext[l] = aall_comboshanum[plaintext[l]]
		
	#print(plaintext)			#now numbers
	
	for l in range(len(plaintext)):
		plaintext[l] += key
		if plaintext[l] > 26:
			plaintext[l] -= 26

	for l in range(len(plaintext)):
		plaintext[l] = numaall_combosha[plaintext[l]]
	
	# merge into single string
	print(list_to_string(plaintext))
	
	return None ####################################

#yeah I forgot how this works and I'm too tired rn to figure it out but it works.
def check_keys(phrase, key):
	for l in range(len(phrase)):
		try:
			phrase[l] = aall_comboshanum[phrase[l]]
		except KeyError:
			pass
		
	for l in range(len(phrase)):
		try:
			phrase[l] -= key
			if phrase[l] < 1:
				phrase[l] += 26
		except KeyError:
			pass
		except TypeError:
			pass
	
	for l in range(len(phrase)):
		try:
			phrase[l] = numaall_combosha[phrase[l]]
		except KeyError:
			pass
		
	return list_to_string(phrase)
	
	
#Decryption Function
def decrypt(inp, key):		################
	#Take Input
	ctext = list(inp)
	#Check if user has the key.
	if key != None:
		for l in range(len(ctext)):
			ctext[l] = aall_comboshanum[ctext[l]]
		#rotates text by key
		for l in range(len(ctext)):
			ctext[l] -= key
			if ctext[l] < 1:
				#rotation is done by subtraction, if goes before "a" this will move it to the end of the aall_comboshabet to move backwards
				ctext[l] += 26
		#convert numeric values back to letters
		for l in range(len(ctext)):
			ctext[l] = numaall_combosha[ctext[l]]
		#print and exit	
		#print(list_to_string(ctext))
		return None ################################################
		
	#if user doesn't give a key, solve for all possible combinations
	else:
		key = 1
		all_combos = []
		#append all 26 combinations to an array
		while key <= 26:
			copy_ctext = ctext[:]
			all_combos.append(check_keys(copy_ctext, key))
			key += 1
			
		return all_combos
	
def Ceasar():
	print("Welcome to Mitch's ceasar cipher!")
	while (1 == 1):
		inp = input("Encrypt (E) or Decrypt (D): ")
		if inp.lower() == "e":
			encrypt(input("Enter text to decrypt: ").lower())
		elif inp.lower() == "d":
			decrypt(input("Enter text to decrypt: ").lower())
		else:
			print("I did not recognize your input. Try agian.\n")
		
#Ceasar()