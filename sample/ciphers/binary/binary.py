#Binary to Plaintext


def string_decode(input, length=8): #binary to plaintext
	input_l = [input[i:i+length] for i in range(0,len(input),length)]
	return ''.join([chr(int(c,base=2)) for c in input_l])

def decrypt(ciphertext, key=None):
	#change input to just "0" and "1" if applicable
	characters_appened = [item for item in list(ciphertext) if item in ["0","1"]]
	ciphertext = ""
	for char in characters_appened:
		ciphertext+=char
	#iterates over lengths of 4->10
	counter = 4
	all_combos = []
	while counter < 11:
		all_combos.append(string_decode(ciphertext, counter))
		counter+=1
	return all_combos
	