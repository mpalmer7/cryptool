#Binary to Plaintext


def string_decode(input, length=8):
		input_l = [input[i:i+length] for i in range(0,len(input),length)]
		return ''.join([chr(int(c,base=2)) for c in input_l])

#key is unused
def decrypt(ciphertext, key):
	#get number of character types


	ciphertext_characters = list(ciphertext)
	characters_appened = [item for item in ciphertext_characters if item in ["0","1"]]
	ciphertext = ""
	for char in characters_appened:
		ciphertext+=char
	
	counter = 2
	all_combos = []
	while counter < 17:
		all_combos.append(string_decode(ciphertext, counter))
		counter+=1
	
	if len(all_combos) != 0:
		return all_combos
	else:
		return []
	