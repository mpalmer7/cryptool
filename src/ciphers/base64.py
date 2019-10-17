from base64 import b64decode, b64encode
import binascii


def decrypt(ciphertext, b=None):
	if ciphertext.startswith("b'") and ciphertext.endswith("'"):
		ciphertext = ciphertext[2:-1]  # fixes formatting
	try:
		yield b64decode(ciphertext).decode()
	except binascii.Error:
		pass

def encrypt(plaintext, key=None):
	try:
		return b64encode(plaintext.encode()).decode()
	except binascii.Error:
		print("ERROR in base64 encryption function")
		exit()