#Binary to Plaintext


def string_decode(input, length=8): #binary to plaintext
		input_l = [input[i:i+length] for i in range(0,len(input),length)]
		return ''.join([chr(int(c,base=2)) for c in input_l])

def decrypt(ciphertext, key=None):
	#change input to just "0" and "1" if applicable
	ciphertext_characters = list(ciphertext)
	characters_appened = [item for item in ciphertext_characters if item in ["0","1"]]
	ciphertext = ""
	for char in characters_appened:
		ciphertext+=char
	#iterates over lengths of 2->12
	counter = 2
	all_combos = []
	while counter < 13:
		all_combos.append(string_decode(ciphertext, counter))
		counter+=1
	return all_combos
	