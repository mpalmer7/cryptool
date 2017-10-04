import base64
import binascii

def decrypt(ciphertext, b=None):
	try:
		return [str(base64.b64decode(ciphertext))]
	except binascii.Error:
		print("ERROR in base64: Incorrect formatting of input.")
		return []

	#Base64    length divisible by 4, sometimes has “=” at the end