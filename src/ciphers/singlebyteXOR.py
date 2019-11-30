# Single Byte XOR
import binascii


def decrypt(inp_obj):
    try:
        encoded = binascii.unhexlify(inp_obj.string)
    except binascii.Error:
        # print("ERROR in base64: Incorrect formatting of input.")
        return []

    plaintext = []
    for xor_key in range(256):
        decoded = ''.join(chr(b ^ xor_key) for b in encoded)
        if decoded.isprintable():
            yield decoded


def encrypt(inp_obj):
    print("single byte XOR encryption not implemented yet.")
    exit()