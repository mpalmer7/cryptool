# Mitchell Palmer
# Updated: 7/1/18
import binascii


def string_decode(inp, length=8):  # binary to plaintext
    input_l = [inp[i:i + length] for i in range(0, len(inp), length)]
    return ''.join([chr(int(c, base=2)) for c in input_l])

# currently having some issues with the decryption


def decrypt(ciphertext, key=None):
    length = len(ciphertext.split(" ")[0])
    if length > 10:
        length = 8
    # change input to just "0" and "1" if applicable (e.g. there were spaces)
    characters_append = [item for item in list(ciphertext) if item in ["0", "1"]]
    ciphertext = ""
    for char in characters_append:
        ciphertext += char
    return [string_decode(ciphertext, length)]

def encrypt(plaintext):
    ciphertext = ' '.join(format(ord(x), 'b') for x in plaintext)
    return ciphertext
