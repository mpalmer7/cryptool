#Base64    length divisible by 4, sometimes has “=” at the end
import base64
import binascii

def decrypt(ciphertext, b=None):
	try:
		plaintext = str(base64.b64decode(ciphertext))
		if plaintext.startswith("b'") and plaintext.endswith("'"):
			plaintext = plaintext[2:-1] #fix formatting
		return [plaintext]
	except binascii.Error:
		#print("ERROR in base64: Incorrect formatting of input.")
		return []