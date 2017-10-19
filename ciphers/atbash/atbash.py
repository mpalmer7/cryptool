#atbash
def decryplaintext(ciphertext, nullthing=None):
	plaintext = ''
	udict = {'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T',
			'H': 'S', 'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N', 'N': 'M',
			'O': 'L', 'P': 'K', 'Q': 'J', 'R': 'I', 'S': 'H', 'T': 'G', 'U': 'F',
			'V': 'E', 'W': 'D', 'X': 'C', 'Y': 'B', 'Z': 'A'}
	ldict = {'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v', 'f': 'u', 'g': 't',
			'h': 's', 'i': 'r', 'j': 'q', 'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm',
			'o': 'l', 'p': 'k', 'q': 'j', 'r': 'i', 's': 'h', 't': 'g', 'u': 'f',
			'v': 'e', 'w': 'd', 'x': 'c', 'y': 'b', 'z': 'a'}
	#decryption
	for letter in list(ciphertext):
		if letter in udict.keys():
			plaintext += str(udict.get(letter))
		elif letter in ldict.keys():
			plaintext += str(ldict.get(letter))
		else:
			plaintext += letter
	#output
	if plaintext == '':
		return []
	else:
		return [plaintext]
	
	