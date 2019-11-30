import binascii
from base64 import b64decode, b64encode


def decrypt(inp_obj):
	"""Takes in base64 encoded data, either with b'xxxxx' or just xxxxx, and returns the decoded string."""
	ciphertext = inp_obj.string
	if ciphertext.startswith("b'") and ciphertext.endswith("'"):
		ciphertext = ciphertext[2:-1]  # fixes formatting; data input is always of type(str)
	try:
		yield b64decode(ciphertext).decode()
	except binascii.Error:
		pass
	except UnicodeDecodeError:
		pass


def encrypt(inp_obj):
	"""Takes in data, casts it as byte, and returns the base64 encoded string."""

	try:
		return b64encode(inp_obj.bytes).decode()
	except binascii.Error:
		print("ERROR in base64 encryption function")
		exit()
