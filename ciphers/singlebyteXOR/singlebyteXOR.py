#Single Byte XOR
import binascii

def decrypt(ctext, temp=None):
	new = ctext[:-3]	#remove newline###########
	ctext = new
	try:
		encoded = binascii.unhexlify(ctext)
	except binascii.Error:
		print("ERROR in base64: Incorrect formatting of input.")
		return []
		
	plaintext = []
	for xor_key in range(256):
		decoded = ''.join(chr(b ^ xor_key) for b in encoded)
		#print(decoded)
		if decoded.isprintable():
			plaintext.append(decoded)
			
	return plaintext