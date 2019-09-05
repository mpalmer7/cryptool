# Single Byte XOR
import binascii


def decrypt(ctext, temp=None):
    try:
        encoded = binascii.unhexlify(ctext)
    except binascii.Error:
        # print("ERROR in base64: Incorrect formatting of input.")
        return []

    plaintext = []
    for xor_key in range(256):
        decoded = ''.join(chr(b ^ xor_key) for b in encoded)
        if decoded.isprintable():
            yield decoded


def encrypt(inp, key=None):
    print("single byte XOR encryption not implemented yet.")
    exit()