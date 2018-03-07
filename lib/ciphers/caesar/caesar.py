#Ceasar Key Decryption
lalpha = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
ualpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
def check_keys(phrase, key):
	decoded = ""
	cipher_index = 0
	for i in range(len(phrase)):
		if phrase[i] in lalpha:
			decoded += lalpha[lalpha.index(phrase[i]) + key] #.index finds first occurence of item
		elif phrase[i] in ualpha:
			decoded += ualpha[ualpha.index(phrase[i]) + key]
		else:
			decoded += phrase[i]
	return decoded
	
def decrypt(inp, key=None):
	ctext = list(inp)
	if key != None:
		return([check_keys(ctext, key)])
	else:#Key not given, try all keys
		all_combos = []
		for key in range(0,26):
			all_combos.append(check_keys(ctext, key))
			key += 1		
		return all_combos
		
def encrypt(plaintext):
	key = int(input("Enter integer to rotate by: "))
	return check_keys(plaintext, key)
	
#def Ceasar():
