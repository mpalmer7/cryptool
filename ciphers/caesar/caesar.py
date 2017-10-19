#Ceasar Key Decryption

let_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
			'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16,
			'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
			'y': 25, 'z': 26, 'A': 27, 'B': 28, 'C': 29, 'D': 30, 'E': 31, 'F': 32, 'G': 33, 'H': 34,
			'I': 35, 'J': 36, 'K': 37, 'L': 38, 'M': 39, 'N': 40, 'O': 41, 'P': 42,
			'Q': 43, 'R': 44, 'S': 45, 'T': 46, 'U': 47, 'V': 48, 'W': 49, 'X': 50,
			'Y': 51, 'Z': 52}
num_to_let = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l',
			13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v',
			23: 'w', 24: 'x', 25: 'y', 26: 'z', 27: 'A', 28: 'B', 29: 'C', 30: 'D', 31: 'E', 32: 'F', 33: 'G', 34: 'H', 35: 'I', 36: 'J', 37: 'K', 38: 'L',
			39: 'M', 40: 'N', 41: 'O', 42: 'P', 43: 'Q', 44: 'R', 45: 'S', 46: 'T', 47: 'U', 48: 'V',
			49: 'W', 50: 'X', 51: 'Y', 52: 'Z'}
			
def list_to_string(ls):
	str = ''
	for char in ls:
		str += char
	return str
			
def encrypt(plaintext):
	key = int(input("Enter integer to rotate by: "))
	#1) Convert letters to numbers.
	for l in range(len(plaintext)):
		plaintext[l] = let_to_num[plaintext[l]]
	#2) Rotate numbers by key.
	for l in range(len(plaintext)):
		if phrase[l] > 26: #uppercase
				phrase[l] += key
				if phrase[l] > 52:
					phrase[l] -= 26
			else:
				phrase[l] += key #lowercase
				if phrase[l] > 26:
					phrase[l] -= 26
	#3) Numbers back to letters.
	for l in range(len(plaintext)):
		plaintext[l] = num_to_let[plaintext[l]]
	return list_to_string(plaintext)

def check_keys(phrase, key):
	#1) Letters to numbers.
	for l in range(len(phrase)):
		try:
			phrase[l] = let_to_num[phrase[l]]
		except KeyError:
			pass
	#2) Rotate letters by key.	
	for l in range(len(phrase)):
		try:
			if phrase[l] > 26: #uppercase
				phrase[l] -= key
				if phrase[l] < 26:
					phrase[l] += 26
			else:
				phrase[l] -= key #lowercase
				if phrase[l] < 1:
					phrase[l] += 26
		except KeyError:
			pass
		except TypeError:
			pass
	#3) Numbers back to letters.
	for l in range(len(phrase)):
		try:
			phrase[l] = num_to_let[phrase[l]]
		except KeyError:
			pass
	return list_to_string(phrase)
	
def decrypt(inp, key=None):
	ctext = list(inp)
	if key != None:
		return([check_keys(ctext, key)])
	else:#Key not given, try all keys
		all_combos = []
		for key in range(1,27):
			all_combos.append(check_keys(ctext, key))
			key += 1		
		return all_combos
	
def Ceasar():
	invoker = False
	while (invoker == False):
		inp = input("Encrypt (E) or Decrypt (D): ")
		if inp.lower() == "e":
			invoker = True
			print(encrypt(input("Enter text to decrypt: ").lower())
		elif inp.lower() == "d":
			invoker = True
			print(decrypt(input("Enter text to decrypt: ").lower()))
		else:
			print("I did not recognize your input. Try agian.\n")